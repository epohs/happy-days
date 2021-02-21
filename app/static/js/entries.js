
hd.entries = {

  get_entry_sliders: function(){

    return document.querySelectorAll(".entry-val-item > .input-wrap input[type='range']");

  },

  update_entry_val: function(slider) {

    input_wrap = slider.closest('.input-wrap');

    entry_val = hd.getPreviousSibling(input_wrap, '.entry-val');

    entry_val.textContent = slider.value;

  }

}
