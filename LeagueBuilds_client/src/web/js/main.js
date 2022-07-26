var text_passive, text_q, text_w, text_e, text_r;
var text_summ1, text_summ2;
var text_primarystyle, text_primaryperk1, text_primaryperk2, text_primaryperk3, text_primaryperk4;
var text_substyle, text_subperk1, text_subperk2;
var src_passive, src_q, src_w, src_e, src_r;
var mode = 'dark';
var flash_on_f = 0;
var color_background_dark = "gray";
var color_background_light = "WhiteSmoke";
var color_document_dark = "dimgray";
var color_document_light = "white";
var color_text_dark = "white";
var color_text_light = "dimgray";
var color_hover_background_dark = "white";
var color_hover_background_light = "dimgray";
var color_hover_text_dark = "dimgray";
var color_hover_text_light = "white";
var color_slash = "tomato";
var role = "";

bind_spells();
bind_summs();
bind_runes();

eel.get_darkmode()(init_mode);
eel.get_import_runes()(init_runes);
eel.get_import_items()(init_items);
eel.get_import_summs()(init_summs);
eel.get_position_flash()(init_flash);

function init_mode(dark) {
    switch_mode();
    if(dark)
    {
        switch_mode();
    }
}

function init_runes(import_runes) {
    if (!import_runes) {
        switch_runes();
    }
}

function init_items(import_items) {
    if (!import_items) {
        switch_items();
    }
}

function init_summs(import_summs) {
    if (!import_summs) {
        switch_summs();
    }
}

function init_flash(flash_on_f) {
    switch_flash_pos();
    if (flash_on_f) {
        switch_flash_pos();
    }
}

function switch_mode() {
    var ul = document.getElementById("sidebar_ul");
    var a = ul.getElementsByTagName("a");
    var items = ul.getElementsByClassName("item");
    var icons = ul.getElementsByClassName("icon");
    if (mode == 'dark')
    {
        mode = 'light';
        document.body.style.background = color_document_light;

        document.getElementById("mode").innerHTML = "Light Mode";
        for (i = 0; i < items.length; i++) {
            items[i].style.color = color_text_light;
        }
        for (i = 0; i < icons.length; i++) {
            icons[i].style.color = color_text_light;
        }
        for (i = 0; i < a.length; i++) {
            a[i].style.backgroundColor = color_background_light;
        }
        var flash_pos_button = document.getElementById("flash_pos_button");
        var fas = flash_pos_button.getElementsByClassName("icon")[0].getElementsByClassName("fa");
        for (i = 0; i < fas.length; i++) {
            if (i % 2 == 1) {fas[i].style.color = color_text_dark;}
            else {fas[i].style.color = color_text_light;}
        }

        document.getElementById("top_navbar").style.backgroundColor = color_background_light;
        document.getElementById("bars_icon").style.color = color_text_light;
        document.getElementById("sidebar_1").style.backgroundColor = color_background_light;

        document.getElementById("force_import_button").style.color = color_text_light;
        var icons = document.getElementById("force_import_button").getElementsByClassName("icon");
        for (i = 0; i < icons.length; i++) {
            icons[i].style.color = color_text_light;
        }

        document.getElementById("position-window").style.backgroundColor = color_background_light;

        var img = document.getElementById("position-list").children;
        for(i = 0; i < img.length; i++){
            img[i].style.background = color_background_light;
        }
        if(role != "")
        {
            document.getElementById(role).style.background = color_background_dark;
        }

        document.getElementById("spell-window").style.backgroundColor = color_background_light;
        document.getElementById("spellorder-window").style.backgroundColor = color_background_light;
        document.getElementById("summoner-window").style.backgroundColor = color_background_light;
        document.getElementById("runes-window").style.backgroundColor = color_background_light;
        
        document.getElementById("spells").style.color = color_text_light;
        document.getElementById("spell-order").style.color = color_text_light;
        document.getElementById("summoner-spells").style.color = color_text_light;
        document.getElementById("runes").style.color = color_text_light;
    }
    else if (mode == 'light')
    {
        mode = 'dark';
        document.body.style.background = color_document_dark;

        document.getElementById("mode").innerHTML = "Dark Mode";
        for (i = 0; i < items.length; i++) {
            items[i].style.color = color_text_dark;
        }
        for (i = 0; i < icons.length; i++) {
            icons[i].style.color = color_text_dark;
        }
        for (i = 0; i < a.length; i++) {
            a[i].style.backgroundColor = color_background_dark;
        }
        var flash_pos_button = document.getElementById("flash_pos_button");
        var fas = flash_pos_button.getElementsByClassName("icon")[0].getElementsByClassName("fa");
        for (i = 0; i < fas.length; i++) {
            if (i % 2 == 1) {fas[i].style.color = color_text_light;}
            else {fas[i].style.color = color_text_dark;}
        }

        document.getElementById("top_navbar").style.backgroundColor = color_background_dark;
        document.getElementById("bars_icon").style.color = color_text_dark;
        document.getElementById("sidebar_1").style.backgroundColor = color_background_dark;
        
        document.getElementById("force_import_button").style.color = color_text_dark;
        var icons = document.getElementById("force_import_button").getElementsByClassName("icon");
        for (i = 0; i < icons.length; i++) {
            icons[i].style.color = color_text_dark;
        }

        document.getElementById("position-window").style.backgroundColor = color_background_dark;

        var img = document.getElementById("position-list").children;
        for(i = 0; i < img.length; i++){
            img[i].style.background = color_background_dark;
        }
        if(role != "")
        {
            document.getElementById(role).style.background = color_hover_background_dark;
        }

        document.getElementById("spell-window").style.backgroundColor = color_background_dark;
        document.getElementById("spellorder-window").style.backgroundColor = color_background_dark;
        document.getElementById("summoner-window").style.backgroundColor = color_background_dark;
        document.getElementById("runes-window").style.backgroundColor = color_background_dark;

        document.getElementById("spells").style.color = color_text_dark;
        document.getElementById("spell-order").style.color = color_text_dark;
        document.getElementById("summoner-spells").style.color = color_text_dark;
        document.getElementById("runes").style.color = color_text_dark;
    }
}

function toggle_mode() {
    switch_mode();
    
    if (mode == 'dark')
    {
        var mode_button = document.getElementById("mode_button");
        mode_button.style.backgroundColor = color_hover_background_dark;
        mode_button.getElementsByClassName("item")[0].style.color = color_hover_text_dark;
        mode_button.getElementsByClassName("icon")[0].style.color = color_hover_text_dark;
    }
    else if (mode == 'light')
    {
        var mode_button = document.getElementById("mode_button");
        mode_button.style.backgroundColor = color_hover_background_light;
        mode_button.getElementsByClassName("item")[0].style.color = color_hover_text_light;
        mode_button.getElementsByClassName("icon")[0].style.color = color_hover_text_light;
    }

    eel.toggle_darkmode();
}

function create_slash_icon() {
    let element = document.createElement("i");
    element.className = "fa fa-slash fa-stack-1x";
    element.style.color = color_slash;
    return element;
}

function switch_runes() {
    var runes_button = document.getElementById("import_runes_button");
    var runes_icon = runes_button.getElementsByClassName("icon")[0]
    if (runes_icon.children.length > 1) {
        runes_icon.children[1].remove();
    }
    else {
        var slash_icon = create_slash_icon();
        runes_icon.appendChild(slash_icon);
    }
}

function toggle_runes() {
    switch_runes();
    
    eel.toggle_import_runes();
}

function switch_summs() {
    var summs_button = document.getElementById("import_summs_button");
    var summs_icon = summs_button.getElementsByClassName("icon")[0]
    if (summs_icon.children.length > 1) {
        summs_icon.children[1].remove();
    }
    else {
        var slash_icon = create_slash_icon();
        summs_icon.appendChild(slash_icon);
    }
}

function toggle_summs() {
    switch_summs();

    eel.toggle_import_summs();
}

function switch_items() {
    var items_button = document.getElementById("import_items_button");
    var items_icon = items_button.getElementsByClassName("icon")[0]
    if (items_icon.children.length > 1) {
        items_icon.children[1].remove();
    }
    else {
        var slash_icon = create_slash_icon();
        items_icon.appendChild(slash_icon);
    }
}

function toggle_items() {
    switch_items();

    eel.toggle_import_items();
}

function create_flash_icon() {
    let element = document.createElement("i");
    if (!flash_on_f) {
        element.className = "fa fa-d fa-stack-1x fa-xs";
    }
    else {
        element.className = "fa fa-f fa-stack-1x fa-xs";
    }

    if (mode == "dark") {
        element.style.color = color_text_light;
    }
    else if (mode == 'light') {
        element.style.color = color_text_dark;
    }

    return element;
}

function switch_flash_pos() {
    var flash_icon = create_flash_icon();

    if (flash_on_f) {
        flash_on_f = false;

        var flash_pos_button = document.getElementById("flash_pos_button");
        var flash_pos_icon = flash_pos_button.getElementsByClassName("icon")[0]
        flash_pos_icon.children[1].remove();
        flash_pos_icon.appendChild(flash_icon);
    }
    else {
        flash_on_f = true;

        var flash_pos_button = document.getElementById("flash_pos_button");
        var flash_pos_icon = flash_pos_button.getElementsByClassName("icon")[0]
        flash_pos_icon.children[1].remove();
        flash_pos_icon.appendChild(flash_icon);
    }
}

function toggle_flash_pos() {
    switch_flash_pos();

    if (mode == "dark") {
        var flash_pos_button = document.getElementById("flash_pos_button");
        flash_pos_button.style.backgroundColor = color_hover_background_dark;
        flash_pos_button.getElementsByClassName("item")[0].style.color = color_hover_text_dark;
        var fas = flash_pos_button.getElementsByClassName("icon")[0].getElementsByClassName("fa");
        for (i = 0; i < fas.length; i++) {
            if (i % 2 == 1) {fas[i].style.color = color_hover_text_light;}
            else {fas[i].style.color = color_hover_text_dark;}
        }
    }
    else if (mode == "light") {
        var flash_pos_button = document.getElementById("flash_pos_button");
        flash_pos_button.style.backgroundColor = color_hover_background_light;
        flash_pos_button.getElementsByClassName("item")[0].style.color = color_hover_text_light;
        var fas = flash_pos_button.getElementsByClassName("icon")[0].getElementsByClassName("fa");
        for (i = 0; i < fas.length; i++) {
            if (i % 2 == 1) {fas[i].style.color = color_hover_text_dark;}
            else {fas[i].style.color = color_hover_text_light;}
        }
    }

    eel.toggle_position_flash();
}

function force_import() {
    eel.force_import();
}

function reset_position() {
    if (mode == 'dark')
    {
        var img = document.getElementById("position-list").children;
        for(i = 0; i < img.length; i++){
            img[i].style.background = color_background_dark;
        }

        document.getElementById(role).style.background = color_hover_background_dark;
    }
    else
    {
        var img = document.getElementById("position-list").children;
        for(i = 0; i < img.length; i++){
            img[i].style.background = color_background_light;
        }

        document.getElementById(role).style.background = color_background_dark;
    } 
}

function force_position(position) {
    eel.force_position(position);
    role = position;
    reset_position();
}

eel.expose(set_position);
function set_position(position) {
    role = position;
    reset_position();
}

function hover_enter_function(element) {
    var items = element.getElementsByClassName("item");
    var icons = element.getElementsByClassName("icon");
    if (mode == 'dark')
    {
        element.style.backgroundColor = color_hover_background_dark;
        for (i = 0; i < items.length; i++) {
            items[i].style.color = color_hover_text_dark;
        }
        for (i = 0; i < icons.length; i++) {
            icons[i].style.color = color_hover_text_dark;
        }
    }
    else if (mode == 'light')
    {
        element.style.backgroundColor = color_hover_background_light;
        for (i = 0; i < items.length; i++) {
            items[i].style.color = color_hover_text_light;
        }
        for (i = 0; i < icons.length; i++) {
            icons[i].style.color = color_hover_text_light;
        }
    }
}

function hover_leave_function(element) {
    var items = element.getElementsByClassName("item");
    var icons = element.getElementsByClassName("icon");
    if (mode == 'dark')
    {
        element.style.backgroundColor = color_background_dark;
        for (i = 0; i < items.length; i++) {
            items[i].style.color = color_text_dark;
        }
        for (i = 0; i < icons.length; i++) {
            icons[i].style.color = color_text_dark;
        }
    }
    else if (mode == 'light')
    {
        element.style.backgroundColor = color_background_light;
        for (i = 0; i < items.length; i++) {
            items[i].style.color = color_text_light;
        }
        for (i = 0; i < icons.length; i++) {
            icons[i].style.color = color_text_light;
        }
    }
}

function hover_enter_function_flash_pos(element) {
    var items = element.getElementsByClassName("item");
    var icons = element.getElementsByClassName("icon");
    if (mode == 'dark')
    {
        element.style.backgroundColor = color_hover_background_dark;
        for (i = 0; i < items.length; i++) {
            items[i].style.color = color_hover_text_dark;
        }
        for (i = 0; i < icons.length; i++) {
            var fas = icons[i].getElementsByClassName("fa");
            for (ii = 0; ii < fas.length; ii++) {
                if (ii % 2 == 1) {fas[ii].style.color = color_hover_text_light;}
                else {fas[ii].style.color = color_hover_text_dark;}
            }
        }
    }
    else if (mode == 'light')
    {
        element.style.backgroundColor = color_hover_background_light;
        for (i = 0; i < items.length; i++) {
            items[i].style.color = color_hover_text_light;
        }
        for (i = 0; i < icons.length; i++) {
            var fas = icons[i].getElementsByClassName("fa");
            for (ii = 0; ii < fas.length; ii++) {
                if (ii % 2 == 1) {fas[ii].style.color = color_hover_text_dark;}
                else {fas[ii].style.color = color_hover_text_light;}
            }
        }
    }
}

function hover_leave_function_flash_pos(element) {
    var items = element.getElementsByClassName("item");
    var icons = element.getElementsByClassName("icon");
    if (mode == 'dark')
    {
        element.style.backgroundColor = color_background_dark;
        for (i = 0; i < items.length; i++) {
            items[i].style.color = color_text_dark;
        }
        for (i = 0; i < icons.length; i++) {
            var fas = icons[i].getElementsByClassName("fa");
            for (ii = 0; ii < fas.length; ii++) {
                if (ii % 2 == 1) {fas[ii].style.color = color_text_light;}
                else {fas[ii].style.color = color_text_dark;}
            }
        }
    }
    else if (mode == 'light')
    {
        element.style.backgroundColor = color_background_light;
        for (i = 0; i < items.length; i++) {
            items[i].style.color = color_text_light;
        }
        for (i = 0; i < icons.length; i++) {
            var fas = icons[i].getElementsByClassName("fa");
            for (ii = 0; ii < fas.length; ii++) {
                if (ii % 2 == 1) {fas[ii].style.color = color_text_dark;}
                else {fas[ii].style.color = color_text_light;}
            }
        }
    }
}

function hover_enter_function_force_import(element) {
    document.getElementById('force_import_button_tooltip').style.visibility = 'visible';

    var icons = element.getElementsByClassName("icon");
    for (i = 0; i < icons.length; i++) {
        icons[i].style.color = color_slash;
    }
}

function hover_leave_function_force_import(element) {
    document.getElementById('force_import_button_tooltip').style.visibility = 'hidden';

    var icons = element.getElementsByClassName("icon");
    if (mode == 'dark')
    {
        element.style.color = color_text_dark;
        for (i = 0; i < icons.length; i++) {
            icons[i].style.color = color_text_dark;
        }
    }
    else if (mode == 'light')
    {
        element.style.color = color_text_light;
        for (i = 0; i < icons.length; i++) {
            icons[i].style.color = color_text_light;
        }
    }
}

function hover_enter_function_roles(element) {
    if(element.id != role)
    {
        if (mode == 'dark')
        {
            element.style.background = color_hover_background_dark;
        }
        else if (mode == 'light')
        {
            element.style.background = color_background_dark;
        }
    }
}

function hover_leave_function_roles(element) {
    if(element.id != role)
    {
        if (mode == 'dark')
        {
            element.style.background = color_background_dark;
        }
        else if (mode == 'light')
        {
            element.style.background = color_background_light;
        }
    }
}

var hamburger = document.querySelector(".hamburger");
hamburger.addEventListener("click", function(){
    document.querySelector("body").classList.toggle("active");
})
document.getElementById("sidebar_1").addEventListener("mouseleave", function(){
    document.querySelector("body").classList.toggle("active");
})

function bind_spells()
{
    document.getElementById("passive").addEventListener("mouseenter", function(){document.getElementById('spell-tooltip-text').innerHTML = text_passive;document.getElementById('spell-tooltip').style.visibility = 'visible';document.getElementById('spell-video').src = src_passive;});
    document.getElementById("passive").addEventListener("mouseleave", function(){document.getElementById('spell-tooltip').style.visibility = 'hidden';});

    document.getElementById("Q").addEventListener("mouseenter", function(){ document.getElementById('spell-tooltip-text').innerHTML = text_q;document.getElementById('spell-tooltip').style.visibility = 'visible';document.getElementById('spell-video').src = src_q;});
    document.getElementById("Q").addEventListener("mouseleave", function(){document.getElementById('spell-tooltip').style.visibility = 'hidden';});

    document.getElementById("W").addEventListener("mouseenter", function(){document.getElementById('spell-tooltip-text').innerHTML = text_w;document.getElementById('spell-tooltip').style.visibility = 'visible';document.getElementById('spell-video').src = src_w;});
    document.getElementById("W").addEventListener("mouseleave", function(){document.getElementById('spell-tooltip').style.visibility = 'hidden';});

    document.getElementById("E").addEventListener("mouseenter", function(){document.getElementById('spell-tooltip-text').innerHTML = text_e;document.getElementById('spell-tooltip').style.visibility = 'visible';document.getElementById('spell-video').src = src_e;});
    document.getElementById("E").addEventListener("mouseleave", function(){document.getElementById('spell-tooltip').style.visibility = 'hidden';});

    document.getElementById("R").addEventListener("mouseenter", function(){document.getElementById('spell-tooltip-text').innerHTML = text_r;document.getElementById('spell-tooltip').style.visibility = 'visible';document.getElementById('spell-video').src = src_r;});
    document.getElementById("R").addEventListener("mouseleave", function(){document.getElementById('spell-tooltip').style.visibility = 'hidden';});
}

function bind_summs()
{
    document.getElementById("summ-1").addEventListener("mouseenter", function(){document.getElementById('summ-tooltip').innerHTML = text_summ1;document.getElementById('summ-tooltip').style.visibility = 'visible';});
    document.getElementById("summ-1").addEventListener("mouseleave", function(){document.getElementById('summ-tooltip').style.visibility = 'hidden';});

    document.getElementById("summ-2").addEventListener("mouseenter", function(){document.getElementById('summ-tooltip').innerHTML = text_summ2;document.getElementById('summ-tooltip').style.visibility = 'visible';});
    document.getElementById("summ-2").addEventListener("mouseleave", function(){document.getElementById('summ-tooltip').style.visibility = 'hidden';});
}

function bind_runes()
{
    document.getElementById("primarystyle").addEventListener("mouseenter", function(){document.getElementById('rune-tooltip').innerHTML = text_primarystyle;document.getElementById('rune-tooltip').style.visibility = 'visible';});
    document.getElementById("primarystyle").addEventListener("mouseleave", function(){document.getElementById('rune-tooltip').style.visibility = 'hidden';});

    document.getElementById("primaryperk1").addEventListener("mouseenter", function(){document.getElementById('rune-tooltip').innerHTML = text_primaryperk1;document.getElementById('rune-tooltip').style.visibility = 'visible';});
    document.getElementById("primaryperk1").addEventListener("mouseleave", function(){document.getElementById('rune-tooltip').style.visibility = 'hidden';});

    document.getElementById("primaryperk2").addEventListener("mouseenter", function(){document.getElementById('rune-tooltip').innerHTML = text_primaryperk2;document.getElementById('rune-tooltip').style.visibility = 'visible';});
    document.getElementById("primaryperk2").addEventListener("mouseleave", function(){document.getElementById('rune-tooltip').style.visibility = 'hidden';});

    document.getElementById("primaryperk3").addEventListener("mouseenter", function(){document.getElementById('rune-tooltip').innerHTML = text_primaryperk3;document.getElementById('rune-tooltip').style.visibility = 'visible';});
    document.getElementById("primaryperk3").addEventListener("mouseleave", function(){document.getElementById('rune-tooltip').style.visibility = 'hidden';});

    document.getElementById("primaryperk4").addEventListener("mouseenter", function(){document.getElementById('rune-tooltip').innerHTML = text_primaryperk4;document.getElementById('rune-tooltip').style.visibility = 'visible';});
    document.getElementById("primaryperk4").addEventListener("mouseleave", function(){document.getElementById('rune-tooltip').style.visibility = 'hidden';});

    document.getElementById("substyle").addEventListener("mouseenter", function(){document.getElementById('rune-tooltip').innerHTML = text_substyle;document.getElementById('rune-tooltip').style.visibility = 'visible';});
    document.getElementById("substyle").addEventListener("mouseleave", function(){document.getElementById('rune-tooltip').style.visibility = 'hidden';});

    document.getElementById("subperk1").addEventListener("mouseenter", function(){document.getElementById('rune-tooltip').innerHTML = text_subperk1;document.getElementById('rune-tooltip').style.visibility = 'visible';});
    document.getElementById("subperk1").addEventListener("mouseleave", function(){document.getElementById('rune-tooltip').style.visibility = 'hidden';});

    document.getElementById("subperk2").addEventListener("mouseenter", function(){document.getElementById('rune-tooltip').innerHTML = text_subperk2;document.getElementById('rune-tooltip').style.visibility = 'visible';});
    document.getElementById("subperk2").addEventListener("mouseleave", function(){document.getElementById('rune-tooltip').style.visibility = 'hidden';});
}

eel.expose(set_spell_img);
function set_spell_img(id, img) {
    document.getElementById(id).src = img;
}

eel.expose(set_title);
function set_title(id, title) {
    document.getElementById(id).innerText = title;
}

eel.expose(set_spell_order);
function set_spell_order(id, img) {
    document.getElementById(id).src = img;
    document.getElementById(id).className = "skillorder";
}

eel.expose(set_summ);
function set_summ(id, img) {
    document.getElementById(id).src = img;
    document.getElementById(id).className = "summ";
}

eel.expose(set_rune);
function set_rune(id, img) {
    document.getElementById(id).src = img;
    document.getElementById(id).className = "rune";
}

eel.expose(set_spell_text);
function set_spell_text(passive, q, w, e, r) {
    text_passive = passive;
    text_q = q;
    text_w = w;
    text_e = e;
    text_r = r;
}

eel.expose(set_spell_src);
function set_spell_src(passive, q, w, e, r) {
    src_passive = passive;
    src_q = q;
    src_w = w;
    src_e = e;
    src_r = r;
}

eel.expose(set_summ_text);
function set_summ_text(summ1, summ2) {
    text_summ1 = summ1; 
    text_summ2 = summ2;
}

eel.expose(set_rune_text);
function set_rune_text(primarystyle, primaryperk1, primaryperk2, primaryperk3, primaryperk4, substyle, subperk1, subperk2) {
    text_primarystyle = primarystyle;
    text_primaryperk1 = primaryperk1;
    text_primaryperk2 = primaryperk2;
    text_primaryperk3 = primaryperk3;
    text_primaryperk4 = primaryperk4;
    text_substyle = substyle;
    text_subperk1 = subperk1;
    text_subperk2 = subperk2;
}

eel.expose(update_available);
function update_available(client_version, server_version) {
    document.getElementById("version").innerHTML = client_version;
    if(client_version != server_version)
    {
        customAlert.alert("Update available at", "https://github.com/CookieDecide/LeagueBuilds/releases/latest", "(" + client_version + " -> " + server_version + ")", "New Update");
    }
}

function CustomAlert(){
    this.alert = function(message, link, version, title){
      document.getElementById("popup").innerHTML = '<div id="dialogoverlay"></div><div id="dialogbox" class="slit-in-vertical"><div><div id="dialogboxhead"></div><div id="dialogboxbody"></div><div id="dialogboxfoot"></div></div></div>';
  
      let dialogoverlay = document.getElementById('dialogoverlay');
      let dialogbox = document.getElementById('dialogbox');
      
      let winH = window.innerHeight;
      dialogoverlay.style.height = winH+"px";
      
      dialogbox.style.top = "100px";
  
      dialogoverlay.style.display = "block";
      dialogbox.style.display = "block";
      
      document.getElementById('dialogboxhead').style.display = 'block';
  
      if(typeof title === 'undefined') {
        document.getElementById('dialogboxhead').style.display = 'none';
      } else {
        document.getElementById('dialogboxhead').innerHTML = '<i class="fa fa-exclamation-circle" aria-hidden="true"></i> '+ title;
      }
      document.getElementById('dialogboxbody').innerHTML = '<div>'+message+'</div><a href="'+link+'" target="_blank" rel="noopener noreferrer">'+link+'</a><div>'+version+'</div>';
      document.getElementById('dialogboxfoot').innerHTML = '<button class="pure-material-button-contained active" onclick="customAlert.ok()">OK</button>';
    }
    
    this.ok = function(){
      document.getElementById('dialogbox').remove();
      document.getElementById('dialogoverlay').remove();
    }
}
  
let customAlert = new CustomAlert();

Element.prototype.remove = function() {
    this.parentElement.removeChild(this);
}
NodeList.prototype.remove = HTMLCollection.prototype.remove = function() {
    for(var i = this.length - 1; i >= 0; i--) {
        if(this[i] && this[i].parentElement) {
            this[i].parentElement.removeChild(this[i]);
        }
    }
}