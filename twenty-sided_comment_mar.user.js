// ==UserScript==
// @name           Twenty-Sided Comment Marker
// @namespace      http://greasemonkey.latte.ca/
// @description    A script to mark comments by Shamus and crew.
// @include        http://www.shamusyoung.com/twentysidedtale*
// ==/UserScript==


var elements = document.getElementsByClassName("bypostauthor");
var index = -1;

function ScrollToElement(theElement) {
  var selectedPosX = 0;
  var selectedPosY = 0;
  while (theElement != null) {
    selectedPosX += theElement.offsetLeft;
    selectedPosY += theElement.offsetTop;
    theElement = theElement.offsetParent;
  }
  window.scrollTo(selectedPosX,selectedPosY);
}


window.addEventListener("keypress", function(evt) {
  if (evt.charCode == "n".charCodeAt(0)) {
    index++;
  } else if (evt.charCode == "b".charCodeAt(0)) {
    index--;
  }
  else
    return;
  index += elements.length;
  index %= elements.length;
  ScrollToElement(elements[index]);
}, false);
