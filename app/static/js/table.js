
// Write on keyup event of keyword input element
 $(document).ready(function(){
 $("#buscarPersona").keyup(function(){
 _this = this;
 // Show only matching TR, hide rest of them
 $.each($("#tablePersona tbody tr"), function() {
 if($(this).text().toLowerCase().indexOf($(_this).val().toLowerCase()) === -1)
 $(this).hide();
 else
 $(this).show();
 });
 });
});

// Write on keyup event of keyword input element
 $(document).ready(function(){
 $("#buscarLibro").keyup(function(){
 _this = this;
 // Show only matching TR, hide rest of them
 $.each($("#tableLibro tbody tr"), function() {
 if($(this).text().toLowerCase().indexOf($(_this).val().toLowerCase()) === -1)
 $(this).hide();
 else
 $(this).show();
 });
 });
});

$(".botonPersona").click(function() {
    // Obtenemos todos los valores contenidos en los <td> de la fila
    // seleccionada
    $(this).parents("tr").find("#ideP").each(function() {
        $("#idPersona").val($(this).html());
    });
    $(this).parents("tr").find("#dniP").each(function() {
        $("#dni").val($(this).html());
    });
    $(this).parents("tr").find("#nombreP").each(function() {
        $("#nombre").val($(this).html());
    });
    $(this).parents("tr").find("#apellidoP").each(function() {
        $("#apellido").val($(this).html());
    });
    const modal_container = document.getElementById('modal_container');
    const close = document.getElementById('btn btn-success');

    close.addEventListener('click', () => {
        modal_container.classList.remove('show');
    });
});

$(".botonLibro").click(function() {
    // Obtenemos todos los valores contenidos en los <td> de la fila
    // seleccionada
    $(this).parents("tr").find("#ideL").each(function() {
        $("#idLibro").val($(this).html());
    });
    $(this).parents("tr").find("#isbnL").each(function() {
        $("#isbn").val($(this).html());
    });
    $(this).parents("tr").find("#librot").each(function() {
        $("#libro").val($(this).html());
    });
    const modal_containerL = document.getElementById('modal_container');
    const closeL = document.getElementById('btn btn-success');
    closeL.addEventListener('click', () => {
        modal_containerL.classList.remove('show');
    });
});

$(".botonDevolucion").click(function() {
    // Obtenemos todos los valores contenidos en los <td> de la fila
    // seleccionada
    $(this).parents("tr").find("#prestamo").each(function() {
        $("#ideprestamo").val($(this).html());
    });
    $(this).parents("tr").find("#estado").each(function() {
        $("#estadoEntregado").val($(this).html());
    });
});



