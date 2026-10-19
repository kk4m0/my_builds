(function(){
const form=document.getElementById('registerForm'), box=document.getElementById('message');
form.addEventListener('submit',async e=>{
 e.preventDefault(); box.innerHTML='';
 const data=Object.fromEntries(new FormData(form).entries());
 try{
  const r=await fetch('/api/customers/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  const out=await r.json();
  if(!r.ok) throw new Error(out.error||'Could not create account.');
  box.innerHTML="<div class='banner info'>"+escapeText(out.message)+" <a href='/book-for-pet'>Request a booking</a></div>";form.reset();
 }catch(err){box.innerHTML="<div class='banner red'>"+escapeText(err.message)+"</div>";}
});
function escapeText(s){const d=document.createElement('div');d.textContent=s;return d.innerHTML;}
})();