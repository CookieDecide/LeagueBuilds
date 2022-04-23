//document.getElementById("passive").addEventListener("mouseover", ()=>{eel.set_tooltip()});
var text_passive, text_q, text_w, text_e, text_r;
var text_summ1, text_summ2;
var text_primarystyle, text_primaryperk1, text_primaryperk2, text_primaryperk3, text_primaryperk4;
var text_substyle, text_subperk1, text_subperk2;

bind_spells();
bind_summs();
bind_runes();


function bind_spells()
{
    document.getElementById("passive").addEventListener("mouseenter", function(){document.getElementById('spell-tooltip').innerHTML = text_passive;document.getElementById('spell-tooltip').style.visibility = 'visible';});
    document.getElementById("passive").addEventListener("mouseleave", function(){document.getElementById('spell-tooltip').style.visibility = 'hidden';});

    document.getElementById("Q").addEventListener("mouseenter", function(){document.getElementById('spell-tooltip').innerHTML = text_q;document.getElementById('spell-tooltip').style.visibility = 'visible';});
    document.getElementById("Q").addEventListener("mouseleave", function(){document.getElementById('spell-tooltip').style.visibility = 'hidden';});

    document.getElementById("W").addEventListener("mouseenter", function(){document.getElementById('spell-tooltip').innerHTML = text_w;document.getElementById('spell-tooltip').style.visibility = 'visible';});
    document.getElementById("W").addEventListener("mouseleave", function(){document.getElementById('spell-tooltip').style.visibility = 'hidden';});

    document.getElementById("E").addEventListener("mouseenter", function(){document.getElementById('spell-tooltip').innerHTML = text_e;document.getElementById('spell-tooltip').style.visibility = 'visible';});
    document.getElementById("E").addEventListener("mouseleave", function(){document.getElementById('spell-tooltip').style.visibility = 'hidden';});

    document.getElementById("R").addEventListener("mouseenter", function(){document.getElementById('spell-tooltip').innerHTML = text_r;document.getElementById('spell-tooltip').style.visibility = 'visible';});
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