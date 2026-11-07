#!/usr/bin/env python3
"""Builds index.html for pittner/manifestation-vision-board.

A single-purpose page for the "manifestation vision board" / "manifestation goals 2027" search intent
(boards are made in December and January): 36 goals in 6 groups (money and abundance, love and
relationships, career and success, health and energy, home and lifestyle, mindset and inner peace),
each with why it matters and a first step; one click opens the free maker prefilled as a phone lock
screen. Plus 12 questions, a 45-minute plan, a box for your own goal, and FAQ.
"""
import html as _html
import json
import pathlib
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/manifestation-vision-board/"
SRC = "ghpages_manifest"
CAMPAIGN = "manifest_2027"

# (group, [(goal, why it matters, a first step for this week)])
GROUPS = [
    ("Money and abundance", [
        ("Earn 20% more in 2027", "A clear number turns a wish for more money into a plan you can act on.", "Write your current monthly income and the exact number that would be 20% more"),
        ("Have a full emergency fund", "Money in the bank changes how calm you feel about everything else.", "Open a separate savings pot and move a first small amount into it today"),
        ("Be debt-free", "Every debt you close is money that starts working for you instead.", "List every debt with its amount and interest rate on one page"),
        ("Get paid what I am worth", "Undercharging is the most common money leak for skilled people.", "Find three real salary or price numbers for your role or service"),
        ("Start a side income", "A second income stream makes you less afraid of losing the first.", "Write three things people already ask you for help with"),
        ("Feel calm when I check my bank account", "Avoiding your account keeps money stress vague and bigger than it is.", "Check your account every morning this week and write one line about it"),
    ]),
    ("Love and relationships", [
        ("Attract a loving partner", "Knowing what you want makes it easier to say no to what you do not.", "Write five qualities that matter to you and one you will not accept"),
        ("Feel closer to my partner", "Small daily attention builds more closeness than rare big gestures.", "Plan one evening this week with phones in another room"),
        ("Have friends who lift me up", "The people around you shape your mood, habits and ambition.", "Message one person you admire and suggest a coffee"),
        ("Heal an important relationship", "One honest conversation can remove years of quiet tension.", "Write what you would want to say, without sending it yet"),
        ("Love myself the way I love others", "How you talk to yourself sets the tone for every other relationship.", "Write down one kind sentence you would say to a friend in your place"),
        ("Make new friends in my city", "Adult friendships need a reason to meet again and again.", "Sign up for one regular class, club or group this week"),
    ]),
    ("Career and success", [
        ("Land my dream job", "A named job title is something you can work toward; a vague wish is not.", "Write the job title, three companies and the month you will apply"),
        ("Get promoted", "Promotions go to people whose results are visible and asked for.", "Ask your manager what exactly the next level would need from you"),
        ("Launch my own business", "A first paying customer is worth more than months of planning.", "Describe your offer in one sentence and show it to three people"),
        ("Be known for my work", "Visible work brings opportunities you could never plan for.", "Share one thing you learned at work this week where people can see it"),
        ("Finish the project I keep putting off", "An unfinished project drains energy every time you think of it.", "Write the next physical step and put a date next to it"),
        ("Work fewer hours for the same pay", "Time is the one thing you cannot earn back later.", "Track where your work hours go for three days"),
    ]),
    ("Health and energy", [
        ("Wake up with energy", "Energy in the morning decides how the rest of the day goes.", "Set a fixed bedtime for this week and keep it five nights in a row"),
        ("Reach a healthy weight", "Feeling good in your body changes how you show up everywhere.", "Write today's weight and one food swap you will make this week"),
        ("Run my first 5K", "A finish line gives training a purpose and a date.", "Walk-run for 20 minutes three times this week"),
        ("Feel strong in my body", "Strength makes everyday life easier and protects you as you age.", "Do 10 squats and 10 push-ups (on knees is fine) every day this week"),
        ("Sleep 8 hours", "Most other goals get easier when you are rested.", "Put your phone outside the bedroom tonight"),
        ("Feel calm instead of anxious", "A calm mind makes better decisions about everything else.", "Try 5 minutes of slow breathing after you wake up for one week"),
    ]),
    ("Home and lifestyle", [
        ("Buy my first home", "A home you own is a plan with a number and a date, not a wish.", "Write the price range, the area and the month you want to start viewing"),
        ("Travel somewhere I have always dreamed of", "Trips that are planned happen; trips that are wished for wait.", "Pick the place and set a price alert for flights there"),
        ("Live in a calm, clutter-free home", "Less stuff means less to clean, store and think about.", "Fill one bag with things you have not used in a year"),
        ("Drive the car I want", "A specific model and price make the savings goal real.", "Write the model, the price and the monthly amount you would need to save"),
        ("Have more free time", "Free time does not appear; it is taken back from something else.", "Name one weekly commitment you could drop or shorten"),
        ("Live closer to nature", "Time outside lowers stress more than almost anything else.", "Plan one walk in a park or forest this weekend"),
    ]),
    ("Mindset and inner peace", [
        ("Believe I deserve good things", "People rarely go after what they secretly feel they do not deserve.", "Write three things you have already achieved that you once doubted"),
        ("Trust my own decisions", "Second-guessing costs more time than most wrong choices.", "Make one small decision today in under one minute and stick to it"),
        ("Stop comparing myself to others", "Comparison hides your own progress from you.", "Mute three accounts that make you feel behind"),
        ("Practise gratitude every day", "Noticing what is good trains your attention to find more of it.", "Write three good things from today before you sleep, for seven days"),
        ("Be more confident", "Confidence grows from small promises to yourself that you keep.", "Do one thing this week that feels slightly uncomfortable"),
        ("Let go of what no longer serves me", "Old habits and grudges take space that new things could use.", "Write one habit you will stop this month and what will replace it"),
    ]),
]

QUESTIONS = [
    "What do I want so much that I have stopped saying it out loud?",
    "What would I go after if I knew it would work?",
    "Which of my goals are really mine, and which belong to someone else?",
    "How do I want to feel on an ordinary Tuesday in December 2027?",
    "What did I already make happen in 2026 that I once only wished for?",
    "Which belief about money, love or work holds me back the most?",
    "Who already lives the life I want, and what do they do every day?",
    "What am I willing to give up to get what I want?",
    "What would make 2027 my best year so far?",
    "Which goal scares me a little, in a good way?",
    "What small action could I take every day for the next 30 days?",
    "If my vision came true, what is the first thing I would do?",
]

PLAN = [
    ("10 minutes: write what you want.", "No limits and no editing. Money, love, work, health, home and how you want to feel."),
    ("15 minutes: answer the questions.", "Go through the 12 questions below. Short, honest answers are enough; nobody else reads them."),
    ("10 minutes: pick three goals.", "Not ten. Choose the three that matter most and write each one in the present tense, as if it is already true."),
    ("10 minutes: make it visible.", "Turn your main goal and its first step into a phone lock screen, so you see it every day and act on it, not only wish for it."),
]

FAQ = [
    ("What should I put on a manifestation vision board?",
     "Put the goal in your own words, written as if it is already true, a first step you can do this week, and your reason why. "
     "This page has 36 goals in 6 groups (money and abundance, love and relationships, career and success, health and energy, home and lifestyle, mindset and inner peace), each with a first step, so you can pick three and make them visible."),
    ("Does a manifestation vision board actually work?",
     "A board does not make things happen by itself. What helps is that you see the goal every day, so you notice chances and choose actions that move you toward it. "
     "That is why every goal here comes with a concrete first step, and the habit that works best is putting it on your phone lock screen."),
    ("How do I manifest with a vision board?",
     "Pick a few clear goals, write them in the present tense, add one action for this week, and put the board where you see it every day. Review it each week and update the next step."),
    ("How many goals should I put on my vision board for 2027?",
     "Three is enough: one big goal, one about how you want to feel, and one small daily habit. Fewer goals get done more often."),
    ("Is the maker free?",
     "Yes. It runs in your browser, needs no account and uploads nothing. Save the image to your phone lock screen or print it."),
    ("Can I make a full manifestation vision board with all my goals?",
     "Yes. Start from your goals in the AI vision board generator: you see a free preview, and unlocking the full-size board is optional (8.99 EUR)."),
]

def e(s):
    return _html.escape(s, quote=True)


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


def maker(goal, step, content):
    return link("/free-vision-board-maker/", goal=goal, step=step, layout="text", mode="wallpaper", utm_content=content)


TOOL = link("/free-vision-board-maker/", mode="wallpaper", layout="text", utm_content="plan_tool")
AI = link("/en/create.php", utm_content="faq_ai")
AI_PLAN = link("/en/create.php", utm_content="plan_ai")
HOME = link("/", utm_content="footer_home")


def slug(s):
    return "-".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


def build():
    count = sum(len(gs) for _, gs in GROUPS)
    nav = " ".join(f'<a class="chip" href="#{slug(g)}">{e(g)}</a>' for g, _ in GROUPS)
    blocks = []
    for g, goals in GROUPS:
        cards = []
        for i, (goal, why, step) in enumerate(goals, 1):
            cid = f"{slug(g)}_{i}"
            cards.append(
                f'      <div class="wcard" id="g-{cid}"><h3>{e(goal)}</h3><p>{e(why)}</p>'
                f'<p class="step"><span>First step this week:</span> {e(step)}</p>'
                f'<a class="btn" href="{e(maker(goal, step, "goal_" + cid))}" data-cta="goal_{cid}">Make it my lock screen</a></div>')
        blocks.append(f'  <section class="grp" id="{slug(g)}">\n    <h2>{e(g)}</h2>\n    <div class="grid">\n'
                      + "\n".join(cards) + "\n    </div>\n  </section>")
    questions = "\n".join(f"    <li>{e(q)}</li>" for q in QUESTIONS)
    plan = "\n".join(f"    <li><b>{e(a)}</b> {e(b)}</li>" for a, b in PLAN)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%NAV%%": nav, "%%GROUPS%%": "\n\n".join(blocks), "%%QUESTIONS%%": questions, "%%PLAN%%": plan,
        "%%FAQ%%": faq_html, "%%LD%%": ld, "%%COUNT%%": str(count), "%%NQ%%": str(len(QUESTIONS)),
        "%%TOOL%%": e(TOOL), "%%AI%%": e(AI), "%%AIPLAN%%": e(AI_PLAN), "%%HOME%%": e(HOME),
        "%%URL%%": URL, "%%SRC%%": SRC, "%%CAMPAIGN%%": CAMPAIGN,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes,", count, "goals")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Manifestation Vision Board 2027: %%COUNT%% Goals to Manifest with a First Step + Free Lock Screen</title>
<meta name="description" content="%%COUNT%% goals to manifest in 2027 (money and abundance, love, career, health and energy, home and lifestyle, mindset), each with a first step for this week, %%NQ%% questions and a 45-minute plan. Free lock screen maker.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="Manifestation vision board 2027 - %%COUNT%% goals to manifest with a first step and a free lock screen">
<meta property="og:description" content="Money, love, career, health, home and mindset goals with a first step, %%NQ%% questions, and a lock screen in one click. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#1D4ED8;--bg:#F8FAFD}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#1E40AF;color:#fff}
.own{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:18px;margin:8px 0 22px}
.own h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.own .row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.3fr) auto;gap:8px;align-items:end}
@media (max-width:760px){.own .row{grid-template-columns:1fr}}
.own label{display:block;font-size:13px;color:var(--muted);margin:0 0 4px}
.own input{width:100%;border:1px solid #D1D5DB;border-radius:10px;padding:10px 12px;font:16px/1.3 inherit;background:#fff}
.own input:focus{outline:2px solid var(--acc);outline-offset:1px;border-color:var(--acc)}
#ownMsg{font-size:13px;color:var(--muted);margin:8px 0 0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px}
.chip{display:inline-block;text-decoration:none;border:1px solid var(--rule);background:#fff;color:#374151;padding:6px 12px;border-radius:999px;font-size:14px}
.chip:hover{border-color:var(--acc);color:var(--acc)}
section.grp{padding:22px 0 8px}
section.grp h2{font:600 24px/1.25 Georgia,serif;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:860px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
.wcard{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:14px 14px 16px;display:flex;flex-direction:column}
.wcard h3{font:600 19px/1.25 Georgia,serif;margin:0 0 6px}
.wcard p{margin:0 0 8px;color:#374151;font-size:15px}
.wcard .step{font-size:14px;color:var(--muted);flex:1}
.wcard .step span{color:var(--acc);font-weight:600}
.wcard .btn{align-self:flex-start}
section.block{padding:30px 0;border-top:1px solid var(--rule);margin-top:20px}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
ol.how,ol.qs{max-width:70ch;color:#374151;padding-left:22px}
ol.how li,ol.qs li{margin:0 0 10px}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Manifestation vision board 2027: %%COUNT%% goals to manifest, each with a first step for this week</h1>
  <p class="lede">A manifestation board only works if it changes what you do, and most boards stop at pretty pictures. Below are %%COUNT%% goals to manifest in 2027, from more money and a loving partner to calm mornings and more confidence, each with why it matters and a first step you can do this week, plus %%NQ%% questions to find out what you really want. Press a goal and it opens in a free maker with the first step under it: save it as your phone lock screen and see it every day until it is real.</p>
  <p class="meta">%%COUNT%% goals in 6 groups &middot; %%NQ%% questions &middot; 45-minute plan &middot; lock screen in one click &middot; free, MIT licensed</p>
</header>

<div class="own" id="own">
  <h2>Already know your goal?</h2>
  <div class="row">
    <div><label for="ownGoal">What I am manifesting in 2027</label><input id="ownGoal" maxlength="120" placeholder="e.g. I earn 5,000 a month doing work I love" autocomplete="off"></div>
    <div><label for="ownStep">First step (optional)</label><input id="ownStep" maxlength="120" placeholder="e.g. Update my CV and send it to one company" autocomplete="off"></div>
    <button class="btn primary" id="ownGo" type="button">Make it my lock screen</button>
  </div>
  <p id="ownMsg">Opens the free maker with your goal filled in. Change colors or layout there, then save it to your phone or print it.</p>
</div>

<nav class="chips" aria-label="Groups">%%NAV%% <a class="chip" href="#questions">%%NQ%% questions</a> <a class="chip" href="#plan">45-minute plan</a></nav>

%%GROUPS%%

<section class="block" id="questions">
  <h2>%%NQ%% questions before you choose what to manifest</h2>
  <p>Answer them alone, with a notebook, in 15 minutes. Be honest, nobody else reads it. The answers that surprise you point to the goals that will actually stick.</p>
  <ol class="qs">
%%QUESTIONS%%
  </ol>
</section>

<section class="block" id="plan">
  <h2>Make your manifestation board in 45 minutes</h2>
  <ol class="how">
%%PLAN%%
  </ol>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="plan_tool">Open the free lock-screen maker</a>
     <a class="btn" href="%%AIPLAN%%" data-cta="plan_ai">Make a full board with all my goals</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
  <p style="margin-top:16px"><a class="btn" href="%%AI%%" data-cta="faq_ai">Make a full manifestation vision board</a></p>
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/dream-home-vision-board/">dream home vision board</a>,
  <a href="https://pittner.github.io/fitness-vision-board/">fitness vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-relationships/">relationships vision board</a>,
  <a href="https://pittner.github.io/travel-vision-board/">travel vision board</a>,
  <a href="https://pittner.github.io/self-care-vision-board/">self care vision board</a>,
  <a href="https://pittner.github.io/money-vision-board/">money vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-weight-loss/">weight loss vision board</a>,
  <a href="https://pittner.github.io/new-year-resolutions-2027/">new year's resolutions 2027</a>,
  <a href="https://pittner.github.io/vision-board-for-career/">career vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-family/">family vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-couples/">vision board for couples</a>,
  <a href="https://pittner.github.io/vision-board-for-small-business/">small business vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-students/">vision board for students</a>,
  <a href="https://pittner.github.io/word-of-the-year-2027/">word of the year 2027</a>,
  <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">54 vision board prompts</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/manifestation-vision-board">source</a>
</footer>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  // Every link to our site carries where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  // Own goal: same prefill as the goal cards (?goal=&step=&layout=text&mode=wallpaper).
  var g=document.getElementById('ownGoal'),s=document.getElementById('ownStep'),msg=document.getElementById('ownMsg');
  function go(){
    var goal=g.value.trim(),step=s.value.trim();
    if(!goal){ msg.textContent='Type your goal first.'; g.focus(); return; }
    var q=new URLSearchParams({goal:goal,layout:'text',mode:'wallpaper',utm_source:P,utm_medium:'referral',
      utm_campaign:'%%CAMPAIGN%%',utm_content:'own_goal',utm_term:'via_'+src});
    if(step) q.set('step',step);
    beacon('cta_click','own_goal');
    location.href='https://visionboard.bemooore.com/free-vision-board-maker/?'+q.toString();
  }
  document.getElementById('ownGo').addEventListener('click',go);
  [g,s].forEach(function(el){ el.addEventListener('keydown',function(e){ if(e.key==='Enter') go(); }); });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
