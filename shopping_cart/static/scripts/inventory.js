
$(document).ready(function(){

   document.session = $('#session').val();
   alert(document.session);
   setTimeout(requestInventory, 100);
    // 单击添加购物车按钮:
  $('#add-button').click(function(event) {
        jQuery.ajax({
            url: '//localhost:8000/cart',
            type: 'POST',
            data: {
                session: document.session,
                action: 'add'
            },
          //  dataType: 'json',
          /*  beforeSend: function(xhr, settings) {
                $(event.target).attr('disabled', 'disabled');
            },*/
            error: function(XMLHttpRequest, textStatus, errorThrown)
            {
             alert(XMLHttpRequest.status);
 alert(XMLHttpRequest.readyState);
 alert(textStatus);
            },
            success: function(data, status, xhr) {
                alert("succes");
                $('#add-to-cart').hide();
                $('#remove-from-cart').show();
                $(event.target).removeAttr('disabled');
            }
        });
    });
    $('#remove-button').click(function(event) {
        jQuery.ajax({
            url: '//localhost:8000/cart',
            type: 'POST',
            data: {
                session: document.session,
                action: 'remove'
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                $(event.target).attr('disabled', 'disabled');
            },
            success: function(data, status, xhr) {
                $('#remove-from-cart').hide();
                $('#add-to-cart').show();
                $(event.target).removeAttr('disabled');
            }
        });
    });
    function requestInventory() {
        alert("get jason");
        jQuery.getJSON('//localhost:8000/cart/status', {session: document.session},
            function(data) {
                 alert(data['inventoryCount']);
                $('#count').html(data['inventoryCount']);
                setTimeout(requestInventory, 0);
               });
    }
});
   /* $('#remove-button').click(function(event) {
        jQuery.ajax({
            url: '//localhost:8000/cart',
            type: 'POST',
            data: {
                session: document.session,
                action: 'remove'
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                $(event.target).attr('disabled', 'disabled');
            },
            success: function(data, status, xhr) {
                $('#remove-from-cart').hide();
                $('#add-to-cart').show();
                $(event.target).removeAttr('disabled');
            }
        });
    });*/
     // 单击移除购物车按钮
    /* $('#remove-button').click(function(event) {
        jQuery.ajax({
            url: '//localhost:8000/cart',
            type: 'POST',
            data: {
                session: document.session,
                action: 'remove'
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                $(event.target).attr('disabled', 'disabled');
            },
            success: function(data, status, xhr) {
                $('#remove-from-cart').hide();
                $('#add-to-cart').show();
                $(event.target).removeAttr('disabled');
            }

            });
        });*/



