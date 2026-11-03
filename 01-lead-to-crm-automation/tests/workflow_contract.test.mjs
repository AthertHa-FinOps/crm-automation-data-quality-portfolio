// Contract checks on the committed n8n export. These are not n8n/HubSpot integration tests.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const WORKFLOW = JSON.parse(fs.readFileSync(path.resolve(HERE, '..', 'workflow.json'), 'utf8'));
const nodes = new Map(WORKFLOW.nodes.map(node => [node.name, node]));
const edges = source => (WORKFLOW.connections[source]?.main ?? []).flat().map(edge => edge.node);
const responseStatus = name => nodes.get(name).parameters.options.responseCode;
const expression = (name, data) => {
  const value = nodes.get(name).parameters.conditions.boolean[0].value1;
  assert.ok(value.startsWith('={{ ') && value.endsWith(' }}'));
  return vm.runInNewContext(value.slice(4, -3), { $json: data });
};
const normalize = body => {
  const code = nodes.get('Validate & Normalize').parameters.jsCode;
  const result = vm.runInNewContext(code, { $input: { first: () => ({ json: { body } }) }, Date });
  return JSON.parse(JSON.stringify(result[0].json));
};

test('all connections point to existing nodes and duplicate names are absent', () => {
  assert.equal(nodes.size, WORKFLOW.nodes.length);
  for (const [source, value] of Object.entries(WORKFLOW.connections)) {
    assert.ok(nodes.has(source), source);
    for (const group of value.main ?? []) {
      for (const edge of group) assert.ok(nodes.has(edge.node), edge.node);
    }
  }
});

test('errors never reach HTTP 200 and validation errors return HTTP 422', () => {
  assert.equal(responseStatus('Respond OK'), 200);
  assert.equal(responseStatus('Respond 422'), 422);
  assert.equal(responseStatus('Respond 502'), 502);
  assert.ok(edges('Outcome CRM Error').includes('Audit Log Error'));
  assert.ok(edges('Audit Log Error').includes('Respond 502'));
  const seen = new Set(), queue = ['Outcome CRM Error'];
  while (queue.length) {
    const node = queue.shift();
    if (seen.has(node)) continue;
    seen.add(node);
    queue.push(...edges(node));
  }
  assert.ok(seen.has('Respond 502'));
  assert.ok(!seen.has('Respond OK'));
  assert.ok(edges('Outcome Rejected').includes('Respond 422'));
});

test('malformed, ambiguous and missing search results fail closed', () => {
  assert.equal(expression('Search Response Valid?', { total: 0, results: [] }), true);
  assert.equal(expression('Search Response Valid?', { total: 1, results: [{ id: '108' }] }), true);
  for (const bad of [{}, {total: 2, results:[{id:'1'}]}, {total:1, results:[]}, {total:1, results:[{}]}, {total:0,results:[{id:'1'}]}]) {
    assert.equal(expression('Search Response Valid?', bad), false, JSON.stringify(bad));
  }
  assert.ok(edges('Search Response Valid?').includes('Outcome CRM Error'));
});

test('create/update responses require a CRM record ID', () => {
  for (const name of ['Create Response Valid?', 'Update Response Valid?']) {
    assert.equal(expression(name, {id:'123'}), true);
    for (const value of [{}, {id:null}, {id:''}, {id:123}]) assert.equal(expression(name, value), false);
    assert.ok(edges(name).includes('Outcome CRM Error'));
  }
});

test('invalid lead input is rejected before CRM operations', () => {
  for (const [payload, error] of [
    [{email:''}, 'MISSING_EMAIL'],
    [{email:'not-an-address'}, 'INVALID_EMAIL'],
    [{email:'test@example.com',phone:'12345'}, 'INVALID_PHONE']
  ]) {
    const result = normalize(payload);
    assert.equal(result.valid, false);
    assert.ok(result.errors.includes(error));
  }
  const ok = normalize({email:'  TEST@EXAMPLE.COM  ',phone:' +1 (416) 555-0105 ',first_name:'  jane  DOE '});
  assert.equal(ok.valid, true);
  assert.equal(ok.lead.email, 'test@example.com');
  assert.equal(ok.lead.phone, '416-555-0105');
  assert.equal(ok.lead.firstname, 'Jane Doe');
});

test('write requests avoid automatic retries and execution log omits raw email', () => {
  for (const name of ['HubSpot Create', 'HubSpot Update']) {
    assert.notEqual(nodes.get(name).retryOnFail, true);
    assert.equal(nodes.get(name).onError, 'continueErrorOutput');
  }
  assert.equal(nodes.get('HubSpot Search').retryOnFail, true);
  for (const name of ['Audit Log','Audit Log Rejected','Audit Log Error']) {
    assert.ok(!nodes.get(name).parameters.jsCode.includes('v.lead.email'));
  }
  assert.equal(nodes.get('Notify Agent (replace)').type, 'n8n-nodes-base.noOp');
  assert.equal(nodes.get('Lead Webhook').parameters.authentication, undefined);
});
