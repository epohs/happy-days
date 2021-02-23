
hd.entries = {

  get_entry_sliders: function(){

    return document.querySelectorAll(".entry-val-item > .input-wrap input[type='range']");

  },

  update_entry_val: function(slider) {

    input_wrap = slider.closest('.input-wrap');

    entry_val = hd.getPreviousSibling(input_wrap, '.entry-val');
    
    cur_val = parseFloat(slider.value);
    
    nice_val = (cur_val == '0' || cur_val == '5.0' ) ? parseInt(cur_val) : cur_val.toFixed(1);

    entry_val.textContent = nice_val;

  }

}
