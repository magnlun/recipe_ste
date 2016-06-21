    function loadDoc(name, url) {
        "use strict";
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (xhttp.readyState === 4 && xhttp.status === 200) {
                document.getElementById("content").innerHTML = xhttp.responseText;
                var menu = document.getElementById("menu").childNodes;
                for (var i = 0; i < menu.length; i += 1) {
                    if( menu[i].id === "selected" )
                    {
                        menu[i].id = "";
                    }
                    if( menu[i].innerHTML === name ) {
                        menu[i].id = "selected";
                    }
                }
            }
        };
        xhttp.open("GET", url, true);
        xhttp.send();
    }
        function addRecipe(url) {
            var form = document.forms["recipe"];
            var recipe = {};
            recipe.name = form.name.value;
            recipe.description = form.description.value;
            recipe.time = form.time.value;
            recipe.time_unit = form.time_unit.options[ form.time_unit.selectedIndex ].text
            recipe.category = getSelectValues(form.category);
            recipe.source = form.source.value;
            recipe.moments = [];
            formMoments = document.getElementById("moment").children;
            for( var i = 0; i < formMoments.length; i++ ) {
                var prefix = "id_" + i + "-";
                var moment = {};
                moment.name = document.getElementById( prefix + "name").value;
                moment.extra_ingredients = getSelectValues(document.getElementById( prefix + "extra_ingredients") )
                moment.instructions = document.getElementById( prefix + "instructions" ).value;
                momentQuantities = formMoments[i].getElementsByTagName("fieldset");
                moment.ingredients = [];
                for( var j = 0; j < momentQuantities.length; j++ ) {
                    var quantity = {};
                    quantity.amount = momentQuantities[j].querySelectorAll('[name=amount]')[0].value;
                    quantity.unit = momentQuantities[j].querySelectorAll('[name=unit]')[0].value;
                    quantity.ingredient = $(momentQuantities[j].querySelectorAll('[name=ingredient]')[0]).find(":selected").text();
                    quantity.comment = momentQuantities[j].querySelectorAll('[name=comment]')[0].value;
                    moment.ingredients[j] = quantity;
                }
                recipe.moments[i] = moment;
            }

            var json = JSON.stringify(recipe);
            $.ajax( {
                url: url,
                contentType: 'application/json',
                data: json,
                method: "POST",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("Authorization", "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1hZ251cyIsImV4cCI6MTQ2NzA1NTk2MSwiZW1haWwiOiJtYWdudXMubHVuZGJlcmdAcHdueS5zZSIsInVzZXJfaWQiOjF9.DFCmcYnE0XtCKWNw9ri6b5ideavN2bwU6xwDBMgNw9s");
                },
                error: function(data) {
                    document.forms["recipe"].description.value = data;
                },
                success: function(data) {
                    document.forms["recipe"].description.value = data;
                }
            });
        }

        function getSelectValues(select) {
          var result = [];
          var options = select && select.options;
          var opt;

          for (var i=0, iLen=options.length; i<iLen; i++) {
            opt = options[i];

            if (opt.selected) {
              result.push(opt.text);
            }
          }
          return result;
        }

    function loadRecipe(url, button) {
        "use strict";
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (xhttp.readyState === 4 && xhttp.status === 200) {
                document.getElementById("recipe").innerHTML = xhttp.responseText;
                document.getElementById("selected").onclick();
            }
        };
        var old = document.getElementById("bold");
        if( old !== null )
        {
            old.id = "";
        }
        button.id = "bold";
        xhttp.open("GET", url, true);
        xhttp.send();
    }