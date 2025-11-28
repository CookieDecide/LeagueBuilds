// Champion data storage - separate for each champion
var championData = {
    1: {
        text_passive: '', text_q: '', text_w: '', text_e: '', text_r: '',
        text_summ1: '', text_summ2: '',
        text_item1: '', text_item2: '', text_item3: '', text_item4: '', text_item5: '', text_item6: '', text_item7: '', text_item8: '', text_item9: '',
        text_start_item1: '', text_start_item2: '', text_start_item3: '',
        text_boot1: '', text_boot2: '', text_boot3: '',
        text_core_item1: '', text_core_item2: '', text_core_item3: '', text_core_item4: '', text_core_item5: '', text_core_item6: '',
        text_primarystyle: '', text_primaryperk1: '', text_primaryperk2: '', text_primaryperk3: '', text_primaryperk4: '',
        text_substyle: '', text_subperk1: '', text_subperk2: '',
        src_passive: '', src_q: '', src_w: '', src_e: '', src_r: '',
        rune_page: 'rune_1_1',
        runes: []
    },
    2: {
        text_passive: '', text_q: '', text_w: '', text_e: '', text_r: '',
        text_summ1: '', text_summ2: '',
        text_item1: '', text_item2: '', text_item3: '', text_item4: '', text_item5: '', text_item6: '', text_item7: '', text_item8: '', text_item9: '',
        text_start_item1: '', text_start_item2: '', text_start_item3: '',
        text_boot1: '', text_boot2: '', text_boot3: '',
        text_core_item1: '', text_core_item2: '', text_core_item3: '', text_core_item4: '', text_core_item5: '', text_core_item6: '',
        text_primarystyle: '', text_primaryperk1: '', text_primaryperk2: '', text_primaryperk3: '', text_primaryperk4: '',
        text_substyle: '', text_subperk1: '', text_subperk2: '',
        src_passive: '', src_q: '', src_w: '', src_e: '', src_r: '',
        rune_page: 'rune_1_2',
        runes: []
    }
};

var mode = 'dark';
var flash_on_f = 0;
var color_slash = "tomato";
var role_1 = "";
var role_2 = "";
var activeChampion = 1;

// Initialize event bindings for both champions
bind_spells(1);
bind_spells(2);
bind_summs(1);
bind_summs(2);
bind_runes(1);
bind_runes(2);
bind_items(1);
bind_items(2);
bind_start_items(1);
bind_start_items(2);

eel.get_darkmode()(init_mode);
eel.get_import_runes()(init_runes);
eel.get_import_items()(init_items);
eel.get_import_summs()(init_summs);
eel.get_position_flash()(init_flash);

function init_mode(dark) {
    switch_mode();
    if(!dark) {
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

function init_flash(flash_on_f_val) {
    switch_flash_pos();
    if (flash_on_f_val) {
        switch_flash_pos();
    }
}

function switch_mode() {
    document.documentElement.setAttribute('data-theme', mode);
    if (mode == 'dark') {
        mode = 'light';
    } else {
        mode = 'dark';
    }
}

function toggle_mode() {
    switch_mode();
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
    } else {
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
    } else {
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
    } else {
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
    } else {
        element.className = "fa fa-f fa-stack-1x fa-xs";
    }
    element.style.color = "var(--color_hover_text)";
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
    } else {
        flash_on_f = true;
        var flash_pos_button = document.getElementById("flash_pos_button");
        var flash_pos_icon = flash_pos_button.getElementsByClassName("icon")[0]
        flash_pos_icon.children[1].remove();
        flash_pos_icon.appendChild(flash_icon);
    }
}

function toggle_flash_pos() {
    switch_flash_pos();

    var flash_pos_button = document.getElementById("flash_pos_button");
    flash_pos_button.style.backgroundColor = "var(--color_hover_background)";
    flash_pos_button.getElementsByClassName("item")[0].style.color = "var(--color_hover_text)";
    var fas = flash_pos_button.getElementsByClassName("icon")[0].getElementsByClassName("fa");
    for (i = 0; i < fas.length; i++) {
        if (i % 2 == 1) {fas[i].style.color = "var(--color_text)";}
        else {fas[i].style.color = "var(--color_hover_text)";}
    }

    eel.toggle_position_flash();
}

function force_import() {
    eel.force_import();
}

function reset_position(championNum) {
    var img = document.getElementById("position-list_" + championNum).children;
    for(i = 0; i < img.length; i++){
        img[i].style.background = "var(--color_background)";
    }

    var role = championNum === 1 ? role_1 : role_2;
    if (role != "") {
        var roleElement = document.getElementById(role + "_" + championNum);
        if (roleElement) {
            roleElement.style.background = "var(--color_hover_background)";
        }
    }
}

function force_position(championNum, position) {
    eel.force_position(championNum, position);
    if (championNum === 1) {
        role_1 = position;
    } else {
        role_2 = position;
    }
    reset_position(championNum);
}

eel.expose(set_position);
function set_position(championNum, position) {
    if (championNum === 1) {
        role_1 = position;
    } else {
        role_2 = position;
    }
    reset_position(championNum);
}

function reset_runes(championNum) {
    var img = document.getElementById("rune-list_" + championNum).children;
    for(i = 0; i < img.length; i++){
        img[i].style.background = "var(--color_background)";
        img[i].style.color = "var(--color_text)";
    }

    document.getElementById(championData[championNum].rune_page).style.background = "var(--color_hover_background)";
    document.getElementById(championData[championNum].rune_page).style.color = "var(--color_hover_text)";
}

function select_runes(championNum, index) {
    pages = ["rune_1_" + championNum, "rune_2_" + championNum, "rune_3_" + championNum];
    eel.update_runes(championNum, index);
    championData[championNum].rune_page = pages[index];
    reset_runes(championNum);
}

eel.expose(init_rune);
function init_rune(championNum) {
    championData[championNum].rune_page = "rune_1_" + championNum;
    reset_runes(championNum);
}

function switchChampion(num) {
    // Hide all champion content
    var champ1 = document.getElementById("champion-1-content");
    var champ2 = document.getElementById("champion-2-content");
    
    champ1.classList.remove("active");
    champ2.classList.remove("active");
    champ1.style.visibility = "hidden";
    champ2.style.visibility = "hidden";
    
    // Remove active class from all tabs
    document.getElementById("tab-1").classList.remove("active");
    document.getElementById("tab-2").classList.remove("active");
    
    // Show selected champion content
    var selectedChamp = document.getElementById("champion-" + num + "-content");
    selectedChamp.classList.add("active");
    selectedChamp.style.visibility = "visible";
    document.getElementById("tab-" + num).classList.add("active");
    
    activeChampion = num;
}

function hover_enter_function(element) {
    var items = element.getElementsByClassName("item");
    var icons = element.getElementsByClassName("icon");

    element.style.backgroundColor = "var(--color_hover_background)";
    element.style.color = "var(--color_hover_text)";
    for (i = 0; i < items.length; i++) {
        items[i].style.color = "var(--color_hover_text)";
    }
    for (i = 0; i < icons.length; i++) {
        icons[i].style.color = "var(--color_hover_text)";
    }
}

function hover_leave_function(element) {
    var items = element.getElementsByClassName("item");
    var icons = element.getElementsByClassName("icon");

    element.style.backgroundColor = "var(--color_background)";
    element.style.color = "var(--color_text)";
    for (i = 0; i < items.length; i++) {
        items[i].style.color = "var(--color_text)";
    }
    for (i = 0; i < icons.length; i++) {
        icons[i].style.color = "var(--color_text)";
    }
}

function hover_enter_function_flash_pos(element) {
    var items = element.getElementsByClassName("item");
    var icons = element.getElementsByClassName("icon");

    element.style.backgroundColor = "var(--color_hover_background)";
    for (i = 0; i < items.length; i++) {
        items[i].style.color = "var(--color_hover_text)";
    }
    for (i = 0; i < icons.length; i++) {
        var fas = icons[i].getElementsByClassName("fa");
        for (ii = 0; ii < fas.length; ii++) {
            if (ii % 2 == 1) {fas[ii].style.color = "var(--color_hover_background)";}
            else {fas[ii].style.color = "var(--color_hover_text)";}
        }
    }
}

function hover_leave_function_flash_pos(element) {
    var items = element.getElementsByClassName("item");
    var icons = element.getElementsByClassName("icon");

    element.style.backgroundColor = "var(--color_background)";
    for (i = 0; i < items.length; i++) {
        items[i].style.color = "var(--color_text)";
    }
    for (i = 0; i < icons.length; i++) {
        var fas = icons[i].getElementsByClassName("fa");
        for (ii = 0; ii < fas.length; ii++) {
            if (ii % 2 == 1) {fas[ii].style.color = "var(--color_background)";}
            else {fas[ii].style.color = "var(--color_text)";}
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

    element.style.color = "var(--color_text)";
    for (i = 0; i < icons.length; i++) {
        icons[i].style.color = "var(--color_text)";
    }
}

function hover_enter_function_roles(element) {
    var parts = element.id.split('_');
    var championNum = parts[1] ? parseInt(parts[1]) : 1;
    var role = championNum === 1 ? role_1 : role_2;
    var baseId = parts[0];
    
    if(baseId != role) {
        element.style.background = "var(--color_hover_background)";
    }
}

function hover_leave_function_roles(element) {
    var parts = element.id.split('_');
    var championNum = parts[1] ? parseInt(parts[1]) : 1;
    var role = championNum === 1 ? role_1 : role_2;
    var baseId = parts[0];
    
    if(baseId != role) {
        element.style.background = "var(--color_background)";
    }
}

function hover_enter_function_runes(element) {
    var championNum = element.id.split('_')[2];
    if(element.id != championData[championNum].rune_page) {
        element.style.background = "var(--color_hover_background)";
        element.style.color = "var(--color_hover_text)";
    }
}

function hover_leave_function_runes(element) {
    var championNum = element.id.split('_')[2];
    if(element.id != championData[championNum].rune_page) {
        element.style.background = "var(--color_background)";
        element.style.color = "var(--color_text)";
    }
}

var hamburger = document.querySelector(".hamburger");
hamburger.addEventListener("click", function(){
    document.querySelector("body").classList.toggle("active");
})
document.getElementById("sidebar_1").addEventListener("mouseleave", function(){
    document.querySelector("body").classList.toggle("active");
})

function bind_spells(championNum) {
    var suffix = "_" + championNum;
    
    document.getElementById("passive" + suffix).addEventListener("mouseenter", function(){
        document.getElementById('spell-tooltip-text' + suffix).innerHTML = championData[championNum].text_passive;
        document.getElementById('spell-tooltip' + suffix).style.visibility = 'visible';
        document.getElementById('spell-video' + suffix).src = championData[championNum].src_passive;
    });
    document.getElementById("passive" + suffix).addEventListener("mouseleave", function(){
        document.getElementById('spell-tooltip' + suffix).style.visibility = 'hidden';
    });

    document.getElementById("Q" + suffix).addEventListener("mouseenter", function(){
        document.getElementById('spell-tooltip-text' + suffix).innerHTML = championData[championNum].text_q;
        document.getElementById('spell-tooltip' + suffix).style.visibility = 'visible';
        document.getElementById('spell-video' + suffix).src = championData[championNum].src_q;
    });
    document.getElementById("Q" + suffix).addEventListener("mouseleave", function(){
        document.getElementById('spell-tooltip' + suffix).style.visibility = 'hidden';
    });

    document.getElementById("W" + suffix).addEventListener("mouseenter", function(){
        document.getElementById('spell-tooltip-text' + suffix).innerHTML = championData[championNum].text_w;
        document.getElementById('spell-tooltip' + suffix).style.visibility = 'visible';
        document.getElementById('spell-video' + suffix).src = championData[championNum].src_w;
    });
    document.getElementById("W" + suffix).addEventListener("mouseleave", function(){
        document.getElementById('spell-tooltip' + suffix).style.visibility = 'hidden';
    });

    document.getElementById("E" + suffix).addEventListener("mouseenter", function(){
        document.getElementById('spell-tooltip-text' + suffix).innerHTML = championData[championNum].text_e;
        document.getElementById('spell-tooltip' + suffix).style.visibility = 'visible';
        document.getElementById('spell-video' + suffix).src = championData[championNum].src_e;
    });
    document.getElementById("E" + suffix).addEventListener("mouseleave", function(){
        document.getElementById('spell-tooltip' + suffix).style.visibility = 'hidden';
    });

    document.getElementById("R" + suffix).addEventListener("mouseenter", function(){
        document.getElementById('spell-tooltip-text' + suffix).innerHTML = championData[championNum].text_r;
        document.getElementById('spell-tooltip' + suffix).style.visibility = 'visible';
        document.getElementById('spell-video' + suffix).src = championData[championNum].src_r;
    });
    document.getElementById("R" + suffix).addEventListener("mouseleave", function(){
        document.getElementById('spell-tooltip' + suffix).style.visibility = 'hidden';
    });
}

function bind_summs(championNum) {
    var suffix = "_" + championNum;
    
    document.getElementById("summ-1" + suffix).addEventListener("mouseenter", function(){
        document.getElementById('summ-tooltip' + suffix).innerHTML = championData[championNum].text_summ1;
        document.getElementById('summ-tooltip' + suffix).style.visibility = 'visible';
    });
    document.getElementById("summ-1" + suffix).addEventListener("mouseleave", function(){
        document.getElementById('summ-tooltip' + suffix).style.visibility = 'hidden';
    });

    document.getElementById("summ-2" + suffix).addEventListener("mouseenter", function(){
        document.getElementById('summ-tooltip' + suffix).innerHTML = championData[championNum].text_summ2;
        document.getElementById('summ-tooltip' + suffix).style.visibility = 'visible';
    });
    document.getElementById("summ-2" + suffix).addEventListener("mouseleave", function(){
        document.getElementById('summ-tooltip' + suffix).style.visibility = 'hidden';
    });
}

function bind_runes(championNum) {
    var suffix = "_" + championNum;
    
    document.getElementById("primarystyle" + suffix).addEventListener("mouseenter", function(){
        document.getElementById('rune-tooltip' + suffix).innerHTML = championData[championNum].text_primarystyle;
        document.getElementById('rune-tooltip' + suffix).style.visibility = 'visible';
    });
    document.getElementById("primarystyle" + suffix).addEventListener("mouseleave", function(){
        document.getElementById('rune-tooltip' + suffix).style.visibility = 'hidden';
    });

    document.getElementById("primaryperk1" + suffix).addEventListener("mouseenter", function(){
        document.getElementById('rune-tooltip' + suffix).innerHTML = championData[championNum].text_primaryperk1;
        document.getElementById('rune-tooltip' + suffix).style.visibility = 'visible';
    });
    document.getElementById("primaryperk1" + suffix).addEventListener("mouseleave", function(){
        document.getElementById('rune-tooltip' + suffix).style.visibility = 'hidden';
    });

    document.getElementById("primaryperk2" + suffix).addEventListener("mouseenter", function(){
        document.getElementById('rune-tooltip' + suffix).innerHTML = championData[championNum].text_primaryperk2;
        document.getElementById('rune-tooltip' + suffix).style.visibility = 'visible';
    });
    document.getElementById("primaryperk2" + suffix).addEventListener("mouseleave", function(){
        document.getElementById('rune-tooltip' + suffix).style.visibility = 'hidden';
    });

    document.getElementById("primaryperk3" + suffix).addEventListener("mouseenter", function(){
        document.getElementById('rune-tooltip' + suffix).innerHTML = championData[championNum].text_primaryperk3;
        document.getElementById('rune-tooltip' + suffix).style.visibility = 'visible';
    });
    document.getElementById("primaryperk3" + suffix).addEventListener("mouseleave", function(){
        document.getElementById('rune-tooltip' + suffix).style.visibility = 'hidden';
    });

    document.getElementById("primaryperk4" + suffix).addEventListener("mouseenter", function(){
        document.getElementById('rune-tooltip' + suffix).innerHTML = championData[championNum].text_primaryperk4;
        document.getElementById('rune-tooltip' + suffix).style.visibility = 'visible';
    });
    document.getElementById("primaryperk4" + suffix).addEventListener("mouseleave", function(){
        document.getElementById('rune-tooltip' + suffix).style.visibility = 'hidden';
    });

    document.getElementById("substyle" + suffix).addEventListener("mouseenter", function(){
        document.getElementById('rune-tooltip' + suffix).innerHTML = championData[championNum].text_substyle;
        document.getElementById('rune-tooltip' + suffix).style.visibility = 'visible';
    });
    document.getElementById("substyle" + suffix).addEventListener("mouseleave", function(){
        document.getElementById('rune-tooltip' + suffix).style.visibility = 'hidden';
    });

    document.getElementById("subperk1" + suffix).addEventListener("mouseenter", function(){
        document.getElementById('rune-tooltip' + suffix).innerHTML = championData[championNum].text_subperk1;
        document.getElementById('rune-tooltip' + suffix).style.visibility = 'visible';
    });
    document.getElementById("subperk1" + suffix).addEventListener("mouseleave", function(){
        document.getElementById('rune-tooltip' + suffix).style.visibility = 'hidden';
    });

    document.getElementById("subperk2" + suffix).addEventListener("mouseenter", function(){
        document.getElementById('rune-tooltip' + suffix).innerHTML = championData[championNum].text_subperk2;
        document.getElementById('rune-tooltip' + suffix).style.visibility = 'visible';
    });
    document.getElementById("subperk2" + suffix).addEventListener("mouseleave", function(){
        document.getElementById('rune-tooltip' + suffix).style.visibility = 'hidden';
    });
}

function bind_items(championNum) {
    var suffix = "_" + championNum;
    
    for (let i = 1; i <= 9; i++) {
        document.getElementById("item" + i + suffix).addEventListener("mouseenter", function(){
            document.getElementById('item-tooltip' + suffix).innerHTML = championData[championNum]['text_item' + i];
            document.getElementById('item-tooltip' + suffix).style.visibility = 'visible';
        });
        document.getElementById("item" + i + suffix).addEventListener("mouseleave", function(){
            document.getElementById('item-tooltip' + suffix).style.visibility = 'hidden';
        });
    }
}

function bind_start_items(championNum) {
    var suffix = "_" + championNum;
    
    for (let i = 1; i <= 3; i++) {
        document.getElementById("start-item" + i + suffix).addEventListener("mouseenter", function(){
            document.getElementById('start-tooltip' + suffix).innerHTML = championData[championNum]['text_start_item' + i];
            document.getElementById('start-tooltip' + suffix).style.visibility = 'visible';
        });
        document.getElementById("start-item" + i + suffix).addEventListener("mouseleave", function(){
            document.getElementById('start-tooltip' + suffix).style.visibility = 'hidden';
        });
    }

    for (let i = 1; i <= 3; i++) {
        document.getElementById("boots" + i + suffix).addEventListener("mouseenter", function(){
            document.getElementById('start-tooltip' + suffix + (i > 1 ? 'b' : '')).innerHTML = championData[championNum]['text_boot' + i];
            document.getElementById('start-tooltip' + suffix + (i > 1 ? 'b' : '')).style.visibility = 'visible';
        });
        document.getElementById("boots" + i + suffix).addEventListener("mouseleave", function(){
            document.getElementById('start-tooltip' + suffix + (i > 1 ? 'b' : '')).style.visibility = 'hidden';
        });
    }

    for (let i = 1; i <= 6; i++) {
        document.getElementById("core-item" + i + suffix).addEventListener("mouseenter", function(){
            document.getElementById('start-tooltip' + suffix + (i > 3 ? 'c' : '')).innerHTML = championData[championNum]['text_core_item' + i];
            document.getElementById('start-tooltip' + suffix + (i > 3 ? 'c' : '')).style.visibility = 'visible';
        });
        document.getElementById("core-item" + i + suffix).addEventListener("mouseleave", function(){
            document.getElementById('start-tooltip' + suffix + (i > 3 ? 'c' : '')).style.visibility = 'hidden';
        });
    }
}

// Eel exposed functions with champion number parameter
eel.expose(set_spell_img);
function set_spell_img(championNum, id, img) {
    document.getElementById(id + "_" + championNum).src = img;
}

eel.expose(set_champion_img);
function set_champion_img(championNum, id, img) {
    document.getElementById(id + "_" + championNum).src = img;
    document.getElementById(id + "_" + championNum).style = "width: 100%;height: 100%;";

    document.getElementById("cover").style.visibility = "hidden";
    document.getElementById("champion-tabs").style.visibility = "visible";
    
    var champContent = document.getElementById("champion-" + championNum + "-content");
    champContent.style.visibility = "visible";
    
    // Update tab label with champion name
    if (championNum === 1) {
        document.getElementById("tab-1").classList.add("active");
        document.getElementById("champion-1-content").classList.add("active");
        champContent.style.visibility = "visible";
    } else {
        // Champion 2 should be hidden initially until tab is clicked
        champContent.classList.remove("active");
        champContent.style.visibility = "hidden";
    }
}

eel.expose(set_title);
function set_title(championNum, id, title) {
    document.getElementById(id + "_" + championNum).innerText = title;
}

eel.expose(set_spell_name);
function set_spell_name(championNum, id, index) {
    const names = ["Q", "W", "E", "R"];
    const spell_colors = ["Crimson", "YellowGreen", "DeepSkyBlue", "Gold"];
    document.getElementById(id + "_" + championNum).innerText = names[index-1];
    document.getElementById(id + "_" + championNum).style.color = spell_colors[index-1];
}

eel.expose(set_spell_order);
function set_spell_order(championNum, id, img) {
    document.getElementById(id + "_" + championNum).src = img;
    document.getElementById(id + "_" + championNum).className = "skillorder";
}

eel.expose(set_summ);
function set_summ(championNum, id, img) {
    document.getElementById(id + "_" + championNum).src = img;
    document.getElementById(id + "_" + championNum).className = "summ";
}

eel.expose(set_rune);
function set_rune(championNum, id, img) {
    document.getElementById(id + "_" + championNum).src = img;
    document.getElementById(id + "_" + championNum).className = "rune";
}

eel.expose(set_item);
function set_item(championNum, id, img) {
    document.getElementById(id + "_" + championNum).src = img;
    document.getElementById(id + "_" + championNum).className = "item";
}

eel.expose(set_spell_text);
function set_spell_text(championNum, passive, q, w, e, r) {
    championData[championNum].text_passive = passive;
    championData[championNum].text_q = q;
    championData[championNum].text_w = w;
    championData[championNum].text_e = e;
    championData[championNum].text_r = r;
}

eel.expose(set_spell_src);
function set_spell_src(championNum, passive, q, w, e, r) {
    championData[championNum].src_passive = passive;
    championData[championNum].src_q = q;
    championData[championNum].src_w = w;
    championData[championNum].src_e = e;
    championData[championNum].src_r = r;
}

eel.expose(set_summ_text);
function set_summ_text(championNum, summ1, summ2) {
    championData[championNum].text_summ1 = summ1; 
    championData[championNum].text_summ2 = summ2;
}

eel.expose(set_item_text);
function set_item_text(championNum, item1, item2, item3, item4, item5, item6, item7, item8, item9) {
    championData[championNum].text_item1 = item1; 
    championData[championNum].text_item2 = item2;
    championData[championNum].text_item3 = item3;
    championData[championNum].text_item4 = item4; 
    championData[championNum].text_item5 = item5;
    championData[championNum].text_item6 = item6;
    championData[championNum].text_item7 = item7; 
    championData[championNum].text_item8 = item8;
    championData[championNum].text_item9 = item9;
}

eel.expose(set_start_item_text);
function set_start_item_text(championNum, item1, item2, item3) {
    championData[championNum].text_start_item1 = item1; 
    championData[championNum].text_start_item2 = item2;
    championData[championNum].text_start_item3 = item3;
}

eel.expose(set_boots_text);
function set_boots_text(championNum, item1, item2, item3) {
    championData[championNum].text_boot1 = item1; 
    championData[championNum].text_boot2 = item2;
    championData[championNum].text_boot3 = item3;
}

eel.expose(set_core_item_text);
function set_core_item_text(championNum, item1, item2, item3, item4, item5, item6) {
    championData[championNum].text_core_item1 = item1; 
    championData[championNum].text_core_item2 = item2;
    championData[championNum].text_core_item3 = item3;
    championData[championNum].text_core_item4 = item4; 
    championData[championNum].text_core_item5 = item5;
    championData[championNum].text_core_item6 = item6;
}

eel.expose(set_rune_text);
function set_rune_text(championNum, primarystyle, primaryperk1, primaryperk2, primaryperk3, primaryperk4, substyle, subperk1, subperk2) {
    championData[championNum].text_primarystyle = primarystyle;
    championData[championNum].text_primaryperk1 = primaryperk1;
    championData[championNum].text_primaryperk2 = primaryperk2;
    championData[championNum].text_primaryperk3 = primaryperk3;
    championData[championNum].text_primaryperk4 = primaryperk4;
    championData[championNum].text_substyle = substyle;
    championData[championNum].text_subperk1 = subperk1;
    championData[championNum].text_subperk2 = subperk2;
}

eel.expose(update_available);
function update_available(client_version, server_version) {
    document.getElementById("version").innerHTML = client_version;
    if(client_version != server_version) {
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
