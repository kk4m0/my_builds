(function(){
const form=document.getElementById('customerBookingForm'), box=document.getElementById('message');
const today=new Date();const local=new Date(today.getTime()-today.getTimezoneOffset()*60000).toISOString().slice(0,10);
document.getElementById('startDate').min=local;document.getElementById('endDate').min=local;
document.getElementById('startDate').addEventListener('change',()=>{document.getElementById('endDate').min=document.getElementById('startDate').value||local;});
form.addEventListener('submit',async e=>{
 e.preventDefault();box.innerHTML='';
 const data=Object.fromEntries(new FormData(form).entries());
 try{
  const r=await fetch('/api/customers/booking-request',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  const out=await r.json();if(!r.ok)throw new Error(out.error||'Could not submit booking request.');
  box.innerHTML="<div class='banner info'>"+escapeText(out.message)+"</div>";form.reset();
 }catch(err){box.innerHTML="<div class='banner red'>"+escapeText(err.message)+"</div>";}
});
function escapeText(s){const d=document.createElement('div');d.textContent=s;return d.innerHTML;}
})();