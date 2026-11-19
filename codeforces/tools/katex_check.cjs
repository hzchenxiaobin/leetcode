// 用法: node codeforces/tools/katex_check.cjs codeforces/contests/0001-0100
const fs=require('fs'),path=require('path');
const katex=require('/Users/chenbinbin/GitHub/leetcode/node_modules/katex');
const roots=process.argv.slice(2);
let files=[];
function walk(p){const st=fs.statSync(p); if(st.isDirectory()) for(const f of fs.readdirSync(p)) walk(path.join(p,f)); else if(p.endsWith('.md')) files.push(p);}
for(const r of roots) if(fs.existsSync(r)) walk(r);
let bad=0,total=0;
for(const f of files){
  const src=fs.readFileSync(f,'utf8').replace(/```[\s\S]*?```/g,'');
  const blocks=[...src.matchAll(/\$\$([\s\S]*?)\$\$/g)].map(m=>m[1]);
  const inlines=[...src.replace(/\$\$[\s\S]*?\$\$/g,'').matchAll(/\$([^$\n]+)\$/g)].map(m=>m[1]);
  for(const [t,d] of [...blocks.map(t=>[t,true]),...inlines.map(t=>[t,false])]){ total++;
    try{katex.renderToString(t,{throwOnError:true,strict:'ignore',displayMode:d});}catch(e){bad++;console.log('FAIL',f,JSON.stringify(t.slice(0,70)),e.message.slice(0,100));}
  }
}
console.log('docs',files.length,'formulas',total,'bad',bad);
