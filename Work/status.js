$(function() {
  $jScroller.add("#twitter_container","#twitter","left",5,true);
  $("#twitter").mousemove(function (event) {
    if ($(this).data('drag') == true)
      this.scrollLeft = $(this).data('scrollX') + ($(this).data('x') - event.clientX);
  }).mousedown(function (event) {
    $(this).data('drag', true).data('x', event.clientX).data('scrollX', this.scrollLeft);
  }).mouseup(function () {
    $(this).data('drag', false);
  });

  $.getJSON("http://bwinton.latte.ca/Work/status.cgi", function(ob, status) {
    $("#twitter").html("");
    $("#tweet_tmpl").render(ob.results)
                    .appendTo("#twitter");
    var width = 0;
    $('.tweet').each(function() {
      width += $(this).outerWidth( true );
    });
    $('#twitter').width(width + 25);

    $jScroller.start();
  });
});
