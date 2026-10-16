#!/usr/bin/env python3
"""Submit a tested GitHub push event to stock Coolify, only at current branch HEAD.
Run only from a trusted production push job with needs: all required check jobs.
The secret authenticates this app's webhook; it grants no general API/read access.
"""
import hashlib,hmac,json,os,pathlib,sys,urllib.request,uuid,subprocess,tempfile
sha=os.environ['GITHUB_SHA'];ref=os.environ['GITHUB_REF'];repo=os.environ['GITHUB_REPOSITORY']
branch=os.environ['PRODUCTION_BRANCH'];assert ref=='refs/heads/'+branch
assert len(sha)==40 and all(c in '0123456789abcdef' for c in sha)
req=urllib.request.Request('https://api.github.com/repos/'+repo+'/git/ref/heads/'+branch,headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json'})
with urllib.request.urlopen(req,timeout=30) as r:head=json.load(r)['object']['sha']
if head!=sha:
 print('A newer production commit exists; obsolete run will not deploy.');sys.exit(0)
# Keep the original GitHub event, including exact tested SHA and repository identity.
body=pathlib.Path(os.environ['GITHUB_EVENT_PATH']).read_bytes();event=json.loads(body)
assert event['after']==sha and event['ref']==ref and event['repository']['full_name']==repo
deploy_repo=os.environ.get('DEPLOY_REPOSITORY',repo)
if deploy_repo!=repo:
 # A dedicated write deploy key can update only this private deployment fork.
 # Normal git push refuses history replacement; never force-push.
 assert os.environ.get('COOLIFY_SOURCE_PUSH_KEY')
 with tempfile.TemporaryDirectory() as folder:
  key=pathlib.Path(folder)/'key';key.write_text(os.environ['COOLIFY_SOURCE_PUSH_KEY']);key.chmod(0o600)
  with urllib.request.urlopen('https://api.github.com/meta',timeout=30) as response:keys=json.load(response)['ssh_keys']
  known=pathlib.Path(folder)/'known_hosts';known.write_text(''.join('github.com '+k+'\n' for k in keys))
  command=f'ssh -i {key} -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile={known}'
  subprocess.run(['git','-c','core.sshCommand='+command,'push','git@github.com:'+deploy_repo+'.git',sha+':refs/heads/'+branch],check=True)
 event['repository']['full_name']=deploy_repo
 body=json.dumps(event,separators=(',',':')).encode()
signature=hmac.new(os.environ['COOLIFY_WEBHOOK_SECRET'].encode(),body,hashlib.sha256).hexdigest()
request=urllib.request.Request('https://paper-grid.sebashurtado.com/webhooks/source/github/events/manual',data=body,method='POST',headers={'Content-Type':'application/json','User-Agent':'Framework-Coolify-CI/1.0','X-GitHub-Event':'push','X-GitHub-Delivery':str(uuid.uuid4()),'X-Hub-Signature-256':'sha256='+signature})
with urllib.request.urlopen(request,timeout=60) as r:result=json.load(r)
items=result if isinstance(result,list) else result.get('data',[])
expected=os.environ['COOLIFY_APPLICATION_UUID']
accepted=[x for x in items if isinstance(x,dict) and x.get('application_uuid')==expected and x.get('status')=='success' and x.get('deployment_uuid') and x.get('message')=='Deployment queued.']
# Stock response nests per-application results; require a queued deployment identifier.
encoded=json.dumps(result)
if len(accepted)!=1:raise SystemExit('Coolify did not queue exactly the target app: '+encoded)
print('Stock Coolify accepted exact tested commit '+sha)
print(encoded)
