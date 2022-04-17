//document.getElementById("passive").addEventListener("mouseover", ()=>{eel.set_tooltip()});

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