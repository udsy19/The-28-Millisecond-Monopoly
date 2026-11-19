/* Public interactive sensitivity analysis.
   Scientific source of truth: Python package in src/monopoly.
   No model output represents real quantum throughput or financial returns.
*/
(function () {
  "use strict";
  const $ = (selector) => document.querySelector(selector);
  const speedKmPerMs = 299.792458;
  const distances = [40,100,160,320,640,1200,2400,4000,5600];
  const deadlines = [0.05,0.1,0.2,0.5,1,2,5,10,15,20,25,30,40];
  const descriptions = {
    purple: ["Conditional physics candidate","The model excludes an arriving classical bit and predicts at least one ideal direct-fibre pair per second. It does not establish a market or a loophole-free Bell test."],
    gold: ["Fastest route uncertain","A signal is not ruled out by relativity, but the assumed fibre path misses the deadline. Faster classical routes must be investigated."],
    coral: ["No direct-fibre supply","The optimistic unrepeated optical channel predicts fewer than one received pair per second. Repeaters, satellites or stored entanglement require separate validation."],
    teal: ["Classical bit arrives","Under the assumed route, one bit can arrive before the deadline. A classical strategy then wins this toy CHSH game with certainty."]
  };
  function formatRate(number) {
    if(number >= 100) return number.toLocaleString(undefined,{maximumFractionDigits:0});
    if(number >= 1) return number.toFixed(2);
    return number.toExponential(2);
  }
  function classify(distance,deadline,rate) {
    const vacuum = distance / speedKmPerMs;
    const fibre = vacuum * 1.468 * 1.08;
    const loss = .2 * distance;
    const pairs = rate * Math.pow(10,-loss/10);
    let region;
    if (deadline >= fibre) region = "teal";
    else if (pairs < 1) region = "coral";
    else if (deadline >= vacuum) region = "gold";
    else region = "purple";
    return {vacuum,fibre,loss,pairs,region};
  }
  function regionForForm() {
    const d = +$("#distance").value;
    const t = +$("#deadline").value;
    const rate = Math.pow(10,+$("#rate").value-1);
    return {d,t,rate,result:classify(d,t,rate)};
  }
  function updateFrontier() {
    const {d,t,rate,result:r} = regionForForm();
    $("#distance-value").textContent = d.toLocaleString()+" km";
    $("#deadline-value").textContent = t.toFixed(t%1===0?0:1)+" ms";
    $("#rate-value").textContent = formatRate(rate);
    $("#vacuum-value").textContent = r.vacuum.toFixed(2)+" ms";
    $("#fibre-value").textContent = r.fibre.toFixed(2)+" ms";
    $("#pairs-value").textContent = formatRate(r.pairs);
    $("#loss-value").textContent = r.loss.toLocaleString(undefined,{maximumFractionDigits:1})+" dB";
    $("#frontier-status").textContent = descriptions[r.region][0];
    $("#frontier-description").textContent = descriptions[r.region][1];
    $("#region-dot").style.background = {purple:"#8f82ed",gold:"#d9aa5b",coral:"#d16769",teal:"#21828a"}[r.region];
    $("#frontier-verdict").textContent = "No independently verified trade value or long-distance quantum service has been established.";
    document.querySelectorAll(".heat-cell").forEach((el) => {
      el.classList.toggle("selected",+el.dataset.distance===d && +el.dataset.deadline===t);
    });
    paintGrid(rate);
  }
  function paintGrid(rate) {
    document.querySelectorAll(".heat-cell").forEach((element) => {
      const region = classify(+element.dataset.distance,+element.dataset.deadline,rate).region;
      element.className = "heat-cell "+region;
      element.setAttribute("aria-label",element.dataset.distance+" kilometres; "+element.dataset.deadline+" milliseconds; "+descriptions[region][0]);
    });
  }
  function initializeGrid() {
    const grid = $("#frontier-grid");
    const label = document.createElement("div");
    label.className = "heat-head";
    label.textContent = "ms / km";
    grid.appendChild(label);
    distances.forEach(d => {
      const cell=document.createElement("div");
      cell.className="heat-head";
      cell.textContent=d.toLocaleString();
      grid.appendChild(cell);
    });
    deadlines.forEach(t => {
      const heading=document.createElement("div");
      heading.className="heat-label";
      heading.textContent=t+" ms";
      grid.appendChild(heading);
      distances.forEach(d => {
        const cell=document.createElement("button");
        cell.type="button";
        cell.className="heat-cell";
        cell.dataset.distance=d;
        cell.dataset.deadline=t;
        cell.title=d+" km, "+t+" ms";
        cell.addEventListener("click",()=>{
          $("#distance").value=d;
          $("#deadline").value=t;
          updateFrontier();
          $("#frontier").scrollIntoView({behavior:"smooth",block:"start"});
        });
        grid.appendChild(cell);
      });
    });
  }
  function updateAudit() {
    const q=+$("#filter").value/100;
    const conditional=(.75-.25*q)/(1-.5*q);
    const retained=1-.5*q;
    $("#filter-value").textContent=(100*q).toFixed(2)+"%";
    $("#conditional-value").textContent=(100*conditional).toFixed(2)+"%";
    $("#retained-value").textContent=(100*retained).toFixed(3)+"%";
    $("#conditional-bar").style.width=(100*conditional)+"%";
    $("#retained-bar").style.width=(100*retained)+"%";
  }
  function updateFinance() {
    const p=+$("#bias").value;
    const weights=[(1-p)*(1-p),p*(1-p),p*(1-p),p*p];
    const best=1-Math.min.apply(null,weights);
    const edge=(.82*100+.18*(-100)-.08)-(best*100+(1-best)*(-100)-.001);
    $("#bias-value").textContent=p.toFixed(2);
    $("#classical-bias").textContent=(100*best).toFixed(2)+"%";
    $("#edge-bias").textContent=(edge>=0?"+":"−")+"$"+Math.abs(edge).toFixed(3);
  }
  initializeGrid();
  ["distance","deadline","rate"].forEach(id=>$("#"+id).addEventListener("input",updateFrontier));
  $("#filter").addEventListener("input",updateAudit);
  $("#bias").addEventListener("input",updateFinance);
  updateFrontier(); updateAudit(); updateFinance();
})();
