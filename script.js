// /************************Options famille par categorie*************************/
// const categorieSelect = document.getElementById('categorie');
// const familleSelect = document.getElementById('famille');


// const optionsParCategorie = {
//     "Acte de malveillance": ["Vols", "Incendie volontaire", "Agressions", "Investigations"],
//     "Contrôle": ["CCTV/Jour"],
//     "Demande d'accès": ["Oublie de badge", "Réactivation de badge", "Badge visiteur", "Badge de prestataire"],
//     "Mission": ["Prestataires", "Visiteurs", "Employés"],
//     "Panne technique systeme": ["CCTV", "ATS8600", "SSM", "TRUVISION", "Netvu observer", "Continuum", "Tournique"],
//     "Travaux": ["Nettoyage", "Intervention IT", "Préparation d'évènements"],
//     "Accident": ["Chutes", "Intérieur d'OTA", "Extérieur d'OTA"],
//     "Incident": ["Alarme CDS", "DG(B1)", "Alarme MSC", "Werehouse"],
//     "Demande de sécurisation": ["Véhicules employé en mission", "Véhicules OTA", "Matériel OTA"]
// };


// function mettreAJourFamilleOptions() {
//     const selectedCategorie = categorieSelect.value;
//     const familleOptions = optionsParCategorie[selectedCategorie];

//     familleSelect.innerHTML = '';

//     const defaultOption = document.createElement('option');
//     defaultOption.value = '';
//     defaultOption.setAttribute('hidden', true);
//     defaultOption.setAttribute('disabled', true);
//     defaultOption.setAttribute('selected', true);
//     familleSelect.add(defaultOption);


//     familleOptions.forEach(option => {
//         const newOption = document.createElement('option');
//         newOption.text = option;
//         familleSelect.add(newOption);
//     });
// }


// categorieSelect.addEventListener('change', mettreAJourFamilleOptions);


// mettreAJourFamilleOptions();


function filterFunction(that, event) {
    let container, input, filter, li, input_val;
    container = $(that).closest(".ouvert");
    input_val = container.find("input").val().toUpperCase();

    if (["ArrowDown", "ArrowUp", "Enter"].indexOf(event.key) != -1) {
        keyControl(event, container)
    } else {
        li = container.find("ul li");
        li.each(function (i, obj) {
            if ($(this).text().toUpperCase().indexOf(input_val) > -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });

        container.find("ul li").removeClass("selected");
        setTimeout(function () {
            container.find("ul li:visible").first().addClass("selected");
        }, 100)
    }
}

function keyControl(e, container) {
    if (e.key == "ArrowDown") {

        if (container.find("ul li").hasClass("selected")) {
            if (container.find("ul li:visible").index(container.find("ul li.selected")) + 1 < container.find("ul li:visible").length) {
                container.find("ul li.selected").removeClass("selected").nextAll().not('[style*="display: none"]').first().addClass("selected");
            }

        } else {
            container.find("ul li:first-child").addClass("selected");
        }

    } else if (e.key == "ArrowUp") {

        if (container.find("ul li:visible").index(container.find("ul li.selected")) > 0) {
            container.find("ul li.selected").removeClass("selected").prevAll().not('[style*="display: none"]').first().addClass("selected");
        }
    } else if (e.key == "Enter") {
        container.find("input").val(container.find("ul li.selected").text()).blur();
        onSelect(container.find("ul li.selected").text(), container.find("input"));
    }

    container.find("ul li.selected")[0].scrollIntoView({
        behavior: "smooth",
    });
}

function onSelect(val, inputElement) {
    // Vérifie si la valeur sélectionnée est différente de la valeur actuelle de l'input
    if (inputElement.val() !== val) {
        alert(val); // Affiche la valeur sélectionnée seulement si elle est différente
    }
}

$(".ouvert input").focus(function () {
    $(this).closest(".ouvert").find("ul").show();
    $(this).closest(".ouvert").find("ul li").show();
});
$(".ouvert input").blur(function () {
    let that = this;
    setTimeout(function () {
        $(that).closest(".ouvert").find("ul").hide();
    }, 300);
});

$(document).on('click', '.ouvert ul li', function () {
    $(this).closest(".ouvert").find("input").val($(this).text()).blur();
    onSelect($(this).text(), $(this).closest(".ouvert").find("input"));
});

$(".ouvert ul li").hover(function () {
    $(this).closest(".ouvert").find("ul li.selected").removeClass("selected");
    $(this).addClass("selected");
});