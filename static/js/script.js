function sinAcentos(str){
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g,"");
}

const mayusculasCampos = ['nombre','paterno','materno','curp'];

mayusculasCampos.forEach(id=>{
    const campo=document.querySelector(`input[name='${id}']`);
    if(campo){
        campo.addEventListener('input',()=>{
            campo.value=sinAcentos(campo.value.toUpperCase());
        });
    }
});

const fotoInput=document.getElementById('fotoInput');
const previewFoto=document.getElementById('previewFoto');

function hayFoto(){
    return previewFoto.src && previewFoto.src!=='#' && previewFoto.style.display==='block';
}

fotoInput.addEventListener('change', function(){
    const file=this.files[0];
    if(file){
        const reader=new FileReader();
        reader.onload=function(e){
            previewFoto.src=e.target.result;
            previewFoto.style.display='block';
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('btnTomarFoto').addEventListener('click', function(){
    Swal.fire({
        title:'Tomar foto',
        html:`<video id="video" width="300" height="225" autoplay></video>
              <canvas id="canvas" width="300" height="225" style="display:none;"></canvas>`,
        showCancelButton:true,
        confirmButtonText:'Capturar',
        didOpen:()=>{
            const video=document.getElementById('video');
            navigator.mediaDevices.getUserMedia({video:true})
                .then(stream=>{video.srcObject=stream});
        },
        preConfirm:()=>{
            const video=document.getElementById('video');
            const canvas=document.getElementById('canvas');
            canvas.getContext('2d').drawImage(video,0,0,canvas.width,canvas.height);
            const dataURL=canvas.toDataURL('image/png');
            previewFoto.src=dataURL;
            previewFoto.style.display='block';

            const inputHidden=document.createElement('input');
            inputHidden.type='hidden';
            inputHidden.name='preview_base64';
            inputHidden.value=dataURL;
            document.getElementById('formRegistro').appendChild(inputHidden);
        }
    });
});