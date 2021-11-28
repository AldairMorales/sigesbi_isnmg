$(".botonEditarAutor").click(function() {
    // Obtenemos todos los valores contenidos en los <td> de la fila
    // seleccionada
    $(this).parents("tr").find("#nombreA").each(function() {
        $("#nombre").val($(this).html());
    });
    $(this).parents("tr").find("#idA").each(function() {
        $("#identificador").val($(this).html());
    });
});

$(".botonEditarCategoria").click(function() {
    // Obtenemos todos los valores contenidos en los <td> de la fila
    // seleccionada
    $(this).parents("tr").find("#idC").each(function() {
        $("#identificador").val($(this).html());
    });
    $(this).parents("tr").find("#descripcionC").each(function() {
        $("#descripcion").val($(this).html());
    });
});

$(".botonEditarEditorial").click(function() {
    // Obtenemos todos los valores contenidos en los <td> de la fila
    // seleccionada

    $(this).parents("tr").find("#ideditorial").each(function() {
        $("#identificador").val($(this).html());

    });
    $(this).parents("tr").find("#descripcionE").each(function() {
        $("#descripcion").val($(this).html());
    });
});

$(".botonEditarPersona").click(function() {
    // Obtenemos todos los valores contenidos en los <td> de la fila
    // seleccionada

    $(this).parents("tr").find("#idPersona").each(function() {
        $("#identificador").val($(this).html());
    });
    $(this).parents("tr").find("#nombreP").each(function() {
        $("#nombre").val($(this).html());
    });
    $(this).parents("tr").find("#apellidoP").each(function() {
        $("#apellido").val($(this).html());
    });
    $(this).parents("tr").find("#correoP").each(function() {
        $("#correo").val($(this).html());
    });
    $(this).parents("tr").find("#codigoP").each(function() {
        $("#codigo").val($(this).html());
    });
    $(this).parents("tr").find("#telefonoP").each(function() {
        $("#telefono").val($(this).html());
    });
});

$(".botonEditarUsuario").click(function() {
    // Obtenemos todos los valores contenidos en los <td> de la fila
    // seleccionada

    $(this).parents("tr").find("#idUsuario").each(function() {
        $("#identificador").val($(this).html());
    });
    $(this).parents("tr").find("#nombreU").each(function() {
        $("#nombre").val($(this).html());
    });
    $(this).parents("tr").find("#apellidoU").each(function() {
        $("#apellido").val($(this).html());
    });
    $(this).parents("tr").find("#telefonoU").each(function() {
        $("#telefono").val($(this).html());
    });
});