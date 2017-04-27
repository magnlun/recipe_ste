    function loadDoc(name, url) {
        "use strict";
        $.ajax({
            url: url,
            cache: false,
            success: function(result) {
                $('#content').html(result);
                $('#menu').children().each(function(index) {
                    if (this.id === "selected") {
                        this.id = "";
                    }
                    if (this.innerHTML === name) {
                        this.id = "selected";
                    }
                });
            }
        });
    }

    function addRecipe(url) {
        var form = document.forms["recipe"];
        var recipe = {};
        recipe.name = form.name[0].value;
        recipe.description = form.description.value;
        recipe.time = form.time.value;
        recipe.time_unit = form.time_unit.options[form.time_unit.selectedIndex].text;
        recipe.category = getSelectValues(form.category);
        recipe.source = form.source.value;
        recipe.moments = [];
        formMoments = document.getElementById("moment").children;
        for (var i = 0; i < formMoments.length; i++) {
            var moment = {};
            moment.name = formMoments[i].querySelectorAll('[name=name]')[0].value;
            moment.extra_ingredients = getSelectValues(formMoments[i].querySelectorAll('[name=extra_ingredients]')[0]);
            moment.instructions = formMoments[i].querySelectorAll('[name=instructions]')[0].value;
            momentQuantities = formMoments[i].getElementsByTagName("fieldset");
            moment.ingredients = [];
            for (var j = 0; j < momentQuantities.length; j++) {
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
        $.ajax({
            url: url,
            contentType: 'application/json',
            data: json,
            method: "POST",
            beforeSend: function(xhr) {
                xhr.setRequestHeader("Authorization", "JWT " + Cookies.get("token"));
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

        for (var i = 0, iLen = options.length; i < iLen; i++) {
            opt = options[i];

            if (opt.selected) {
                result.push(opt.text);
            }
        }
        return result;
    }

    function loadRecipe(url, button) {
        "use strict";
        $.ajax({
            url: url,
            cache: false,
            success: function(result) {
                $('#recipe').html(result);
                $('.bold').each(function(index) {
                    $(this).removeClass('bold').addClass('menu');
                });
                button.className = "bold";
            }
        });
    }