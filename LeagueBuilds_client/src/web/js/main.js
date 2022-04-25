//document.getElementById("passive").addEventListener("mouseover", ()=>{eel.set_tooltip()});
var text_passive, text_q, text_w, text_e, text_r;
var text_summ1, text_summ2;
var text_primarystyle, text_primaryperk1, text_primaryperk2, text_primaryperk3, text_primaryperk4;
var text_substyle, text_subperk1, text_subperk2;
var src_passive, src_q, src_w, src_e, src_r;
var mode = 'dark';

bind_spells();
bind_summs();
bind_runes();

function background_color(element)
{
    if (mode == 'dark')
    {
        mode = 'light';
        document.body.style.background = "white";

        document.getElementById("mode").innerHTML = "Light Mode";
        document.getElementById("cog_icon").style.color = "white";
        document.getElementById("mode").style.color = "white";

        document.getElementById("top_navbar").style.backgroundColor = "WhiteSmoke";
        document.getElementById("bars_icon").style.color = "dimgray";
        document.getElementById("sidebar_1").style.backgroundColor = "WhiteSmoke";

        document.getElementById("spell-window").style.backgroundColor = "WhiteSmoke";
        document.getElementById("spellorder-window").style.backgroundColor = "WhiteSmoke";
        document.getElementById("summoner-window").style.backgroundColor = "WhiteSmoke";
        document.getElementById("runes-window").style.backgroundColor = "WhiteSmoke";

        element.style.backgroundColor = "dimgray";
        
        document.getElementById("spells").style.color = "dimgray";
        document.getElementById("spell-order").style.color = "dimgray";
        document.getElementById("summoner-spells").style.color = "dimgray";
        document.getElementById("runes").style.color = "dimgray";
    }
    else if (mode == 'light')
    {
        mode = 'dark';
        document.body.style.background = "dimgray";

        document.getElementById("mode").innerHTML = "Dark Mode";
        document.getElementById("cog_icon").style.color = "dimgray";
        document.getElementById("mode").style.color = "dimgray";

        document.getElementById("top_navbar").style.backgroundColor = "gray";
        document.getElementById("bars_icon").style.color = "white";
        document.getElementById("sidebar_1").style.backgroundColor = "gray";

        document.getElementById("spell-window").style.backgroundColor = "gray";
        document.getElementById("spellorder-window").style.backgroundColor = "gray";
        document.getElementById("summoner-window").style.backgroundColor = "gray";
        document.getElementById("runes-window").style.backgroundColor = "gray";

        element.style.backgroundColor = "white";

        document.getElementById("spells").style.color = "white";
        document.getElementById("spell-order").style.color = "white";
        document.getElementById("summoner-spells").style.color = "white";
        document.getElementById("runes").style.color = "white";
    } else {
    }
}

function hover_enter_function(element){
    if (mode == 'dark')
    {
        element.style.backgroundColor = "white";
        document.getElementById("cog_icon").style.color = "dimgray";
        document.getElementById("mode").style.color = "dimgray";
    }
    else if (mode == 'light')
    {
        element.style.backgroundColor = "dimgray";
        document.getElementById("cog_icon").style.color = "white";
        document.getElementById("mode").style.color = "white";
    }
}
function hover_leave_function(element){
    if (mode == 'dark')
    {
        element.style.backgroundColor = "gray";
        document.getElementById("cog_icon").style.color = "white";
        document.getElementById("mode").style.color = "white";
    }
    else if (mode == 'light')
    {
        element.style.backgroundColor = "WhiteSmoke";
        document.getElementById("cog_icon").style.color = "dimgray";
        document.getElementById("mode").style.color = "dimgray";
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