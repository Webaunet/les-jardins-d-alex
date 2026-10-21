(function(){
  var burger=document.getElementById('burger'),menu=document.getElementById('menu'),toast=document.getElementById('toast'),t;
  function say(m){toast.textContent=m;toast.classList.add('show');clearTimeout(t);t=setTimeout(function(){toast.classList.remove('show')},3200)}
  function setMenu(o){menu.classList.toggle('open',o);burger.setAttribute('aria-expanded',o);burger.setAttribute('aria-label',o?'Fermer le menu':'Ouvrir le menu')}
  burger.addEventListener('click',function(){setMenu(!menu.classList.contains('open'))});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&menu.classList.contains('open')){setMenu(false);burger.focus()}});
  menu.addEventListener('click',function(e){if(e.target.closest('a'))setMenu(false)});
  window.addEventListener('resize',function(){if(window.innerWidth>980)setMenu(false)});

  function copyText(v,after){
    function ok(){say('Copié dans le presse-papiers')}
    function fb(){after&&after();say('Texte sélectionné : appuyez sur Ctrl+C')}
    try{navigator.clipboard.writeText(v).then(ok,fb)}catch(e){fb()}
  }
  document.querySelectorAll('.copy').forEach(function(b){b.addEventListener('click',function(){
    var s=b.previousElementSibling;
    copyText(b.getAttribute('data-copy'),function(){var r=document.createRange(),g=getSelection();r.selectNodeContents(s);g.removeAllRanges();g.addRange(r)});
  })});

  var form=document.getElementById('contact-form');
  if(!form)return;
  var F={nom:'f-nom',tel:'f-tel',mail:'f-mail',commune:'f-commune',type:'f-type',msg:'f-msg'};
  var rules={
    nom:function(v){return v.length>=2?'':'Indiquez votre nom (2 caractères minimum).'},
    tel:function(v){var n=v.replace(/[\s.\-]/g,'');return /^(?:0|\+33|0033)[1-9]\d{8}$/.test(n)?'':'Entrez un numéro français valide, par exemple 06 12 34 56 78.'},
    mail:function(v){return v===''||/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)?'':'Cette adresse e-mail ne semble pas valide, par exemple nom@exemple.fr.'},
    commune:function(v){return v.length>=2?'':'Indiquez la commune du projet.'},
    type:function(v){return v?'':'Choisissez le type de demande.'},
    msg:function(v){return v.length>=10?'':'Décrivez votre demande en quelques mots (10 caractères minimum).'}
  };
  function val(k){return document.getElementById(F[k]).value.trim()}
  function check(k){
    var el=document.getElementById(F[k]),err=document.getElementById('e-'+k),m=rules[k](val(k));
    err.textContent=m;
    if(m){el.setAttribute('aria-invalid','true')}else{el.removeAttribute('aria-invalid')}
    return !m;
  }
  Object.keys(F).forEach(function(k){
    var el=document.getElementById(F[k]);
    el.addEventListener('blur',function(){if(val(k)!==''||el.getAttribute('aria-invalid'))check(k)});
    el.addEventListener('input',function(){if(el.getAttribute('aria-invalid'))check(k)});
  });
  var recap=document.getElementById('recap');
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var first=null;
    Object.keys(F).forEach(function(k){if(!check(k)&&!first)first=k});
    if(first){recap.hidden=true;document.getElementById(F[first]).focus();return}
    var txt='Bonjour, je souhaite vous contacter au sujet de : '+val('type')+'.\n'
      +'Commune : '+val('commune')+'\n'
      +'Message : '+val('msg')+'\n'
      +'Nom : '+val('nom')+'\n'
      +'Téléphone : '+val('tel')+(val('mail')?'\nE-mail : '+val('mail'):'');
    document.getElementById('recap-text').textContent=txt;
    document.getElementById('r-sms').href='sms:+33664103457?body='+encodeURIComponent(txt);
    var mail=document.getElementById('r-mail');
    if(mail)mail.href='mailto:alex.noc78@gmail.com?subject='+encodeURIComponent('Demande de contact : '+val('type'))+'&body='+encodeURIComponent(txt);
    recap.hidden=false;
    recap.scrollIntoView({behavior:'smooth',block:'nearest'});
    document.getElementById('recap-title').focus();
  });
  document.getElementById('r-copy').addEventListener('click',function(){
    var pre=document.getElementById('recap-text');
    copyText(pre.textContent,function(){var r=document.createRange(),g=getSelection();r.selectNodeContents(pre);g.removeAllRanges();g.addRange(r)});
  });
})();
