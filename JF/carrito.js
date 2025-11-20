//variable//
var carritovisible = false;

//cargado//
if(document.readyState=='loading'){
    document.addEventListener('DOMContentLoaded',ready)
}else{
    ready();
}


function ready(){
    //funcionalidad//
    var botonesEliminarItem = document.getElementsByClassName('btn-eliminar');
    for(var i=0; 1 < botonesEliminarItem. length;i++){
        var button = botonesEliminarItem[i];
        button.addEventListener('click',eliminaritemcarrito);
    }
}


//eliminacion//
function eliminaritemcarrito(event){
    var buttonClicked = event.target;
    buttonClicked.parentelement.remove();

    //totalactu elimn//
    actualizarTotalcarrito();
}

//totalact//
function actualizarTotalcarrito(){
    //contenido//
    var carritoContenedor = document.getElementsByClassName('carrito')[0];
    var carritoitems = carritoContenedor.getElementsByClassName('carrito-item');
    var total = 0;

    //elemen//
    for(var i=0; i < carritoitems.length;i++){
        var item = carritoitems[i];
        var precioelemento = item.getElementsByClassName('carrito-item-precio')[0];
        console.log(precioelemento);
        //simbolo//
        var precio = parsefloat(precioelemento.innertext.replace('$','').replace('.',''));
        console.log(precio);
        var cantidaditem = item.getElementsByClassName('carrito-item-cantidad')[0];
        var cantidad = cantidaditem.ariaValueMax;
        console.log(cantidad);
        total = total + (precio * cantidad);
    }
    total = math.round(total*100)/100;
    document.getElementsByClassName('carrito-precio-total')[0].innertext = total;
}