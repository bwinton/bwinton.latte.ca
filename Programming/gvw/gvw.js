var folding = $(".folding");
var previous = folding.html();
current = previous.replace(/# +([0-9]+)(.*)/g, "<div class='fold' pos='$1'>\n" +
			   "<span class='number'>...$1</span>" +
			   "<span class='desc'>$2</span>" +
			   "<span class='dots'>...</span>\n" +
			   "<span class='full'>");
current = current.replace(/# +\/([0-9]+)/g, "</span>\n</div>");
folding.html(current);
$(".fold").click(function(e) {
  e.stopPropagation();
  self = $(this);
  self.children(".full").slideDown();
  next = Number(self.attr("pos")) + 1;
  $(".fold[pos="+next+"] > .desc").fadeIn();
});
$(".fold[pos=1] > .desc").fadeIn();
