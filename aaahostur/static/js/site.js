window.onscroll = function () { hideOnScroll() };
        function hideOnScroll() {
            if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20)
                document.getElementById("up-btn").style.display = "block";
            else
                document.getElementById("up-btn").style.display = "none";
            
            if (document.body.clientWidth > 1300)
                if (document.body.scrollTop > 120 || document.documentElement.scrollTop > 120)
                    document.getElementById("navbar-logo").style.visibility = "visible";
                else
                    document.getElementById("navbar-logo").style.visibility = "hidden";
            else
                document.getElementById("navbar-logo").style.visibility = "visible";
        }

        function goToTop() {
            document.getElementById("up").scrollIntoView();
        }

        function changeCheckboxState(e) {
            let input = e.querySelector("input");
            if (input.getAttribute("checked") === null) input.setAttribute("checked", "");
            else input.removeAttribute("checked");
        }

        function showPNAData(e) {
            window.event.stopPropagation();
            doc = document.getElementById("pna_data");
            inputs = document.querySelectorAll("#pna_data input")
            changeCheckboxState(e);
            if (e.childNodes[1].getAttribute("checked") !== null) {
                doc.classList.remove("dis-none");
                for(let i = 0; i < inputs.length; i++) {
                    inputs[i].setAttribute("required", "");
                }           
            }
            else {
                doc.classList.add("dis-none");
                for(let i = 0; i < inputs.length; i++) {
                    inputs[i].removeAttribute("required");
                }
            }
        }

        function showContactSecundaryData(e){
            doc = document.getElementById("extra-data");
            inputs = document.querySelectorAll("#extra-data input")
            changeCheckboxState(e);
            if (e.childNodes[1].getAttribute("checked") !== null) {
                doc.classList.remove("dis-none");
                for(let i = 0; i < inputs.length; i++) {
                    inputs[i].setAttribute("required", "");
                }
            }
            else {
                doc.classList.add("dis-none");
                for(let i = 0; i < inputs.length; i++) {
                    inputs[i].removeAttribute("required");
                }
            }
        }
        
        function showHandicapData(e) {
            doc = document.getElementById("handicap_data");
            inputs = document.querySelectorAll("#handicap_data input")
            changeCheckboxState(e);
            if (e.childNodes[1].getAttribute("checked") !== null) {
                doc.classList.remove("dis-none");
                for(let i = 0; i < inputs.length; i++) {
                    inputs[i].setAttribute("required", "");
                }
            }
            else {
                doc.classList.add("dis-none");
                for(let i = 0; i < inputs.length; i++) {
                    inputs[i].removeAttribute("required");
                }
            }
        }

        function changeRadioGroupButtonState(rbgName, elem) {
            let radiogroup = document.getElementsByClassName(rbgName);
            for (var i = 0; i < radiogroup.length; i++) {
                if (radiogroup.item(i) === elem.childNodes[1]){
                    radiogroup.item(i).checked = true;
                    radiogroup.item(i).setAttribute("checked", "");
                }
                else {
                    radiogroup.item(i).checked = false;
                    radiogroup.item(i).removeAttribute("checked");
                }
            }
        }

        function showTypeData(e, b) {
            doc = document.getElementById("rbgroup-international-type");
            inputs = document.querySelectorAll("#rbgroup-international-type input")
            changeRadioGroupButtonState("rbgroup-company-type", e);
            if (b) {
                doc.classList.remove("dis-none");
            }
            else {
                doc.classList.add("dis-none");
            }
        }