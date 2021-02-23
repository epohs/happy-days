let hd = {}


hd.getPreviousSibling = function (elem, selector) {

  // Get the next sibling element
  var sibling = elem.previousElementSibling;

  // If there's no selector, return the first sibling
  if (!selector) return sibling;

  // If the sibling matches our selector, use it
  // If not, jump to the next sibling and continue the loop
  while (sibling) {
    if (sibling.matches(selector)) return sibling;
    sibling = sibling.previousElementSibling;
  }

};




document.addEventListener("DOMContentLoaded", function() {

  let sliders = hd.entries.get_entry_sliders();

  if ( sliders.length ) {

    console.log('found sliders.');

    sliders.forEach(item => {

      console.log('attaching to: ' + item.getAttribute('id'));
      
      item.addEventListener( 'input', event => hd.entries.update_entry_val(item) )

    }); // forEach(sliders)

  } // if (sliders)

});