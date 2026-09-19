const http=require('http');const fs=require('fs');
const body=JSON.stringify({model:'deepseek-web',messages:[{role:'user',content:'Responde solo con: OK'}],stream:false});
const t0=Date.now();
const req=http.request({host:'127.0.0.1',port:8765,path:'/v1/chat/completions',method:'POST',headers:{'Content-Type':'application/json','Content-Length':Buffer.byteLength(body)},timeout:180000},r=>{let d='';r.setEncoding('utf8');r.on('data',c=>d+=c);r.on('end',()=>{let ct='';try{ct=JSON.parse(d).choices[0].message.content}catch(e){ct='PARSE_ERR '+d.slice(0,300)}fs.writeFileSync('C:/Users/dza/Desktop/automatico-main/public/_gen7.json',JSON.stringify({status:r.statusCode,ms:Date.now()-t0,len:(ct||'').length,content:(ct||'').slice(0,500)}))})});
req.on('error',e=>fs.writeFileSync('C:/Users/dza/Desktop/automatico-main/public/_gen7.json',JSON.stringify({error:String(e),ms:Date.now()-t0})));
req.on('timeout',()=>{req.destroy();fs.writeFileSync('C:/Users/dza/Desktop/automatico-main/public/_gen7.json',JSON.stringify({error:'TIMEOUT',ms:Date.now()-t0}))});
req.write(body);req.end();
