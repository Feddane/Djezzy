document.addEventListener('DOMContentLoaded', function() {
    function updateFileName() {
        var input = document.getElementById('fileUpload');
        var fileName = input.files.length > 0 ? input.files[0].name : "Aucun fichier disponible";
        document.getElementById('fileName').textContent = fileName;
    }

    const fileLabelElement = document.querySelector('.file-label');
    if (fileLabelElement) {
        fileLabelElement.addEventListener('click', function(event) {
            event.preventDefault();
            document.getElementById('fileUpload').click();
        });
    }

    const fileUploadElement = document.getElementById('fileUpload');
    if (fileUploadElement) {
        fileUploadElement.addEventListener('change', updateFileName);
    }

    const categorieSelect = document.getElementById('categorie');
    const familleSelect = document.getElementById('famille');

    const optionsParCategorie = {
        "Acte de malveillance": ["Vols", "Incendie volontaire", "Agressions", "Investigations"],
        "Contrôle": ["CCTV/Jour"],
        "Demande d'accès": ["Oublie de badge", "Réactivation de badge", "Badge visiteur", "Badge de prestataire"],
        "Mission": ["Prestataires", "Visiteurs", "Employés"],
        "Panne technique systeme": ["CCTV", "ATS8600", "SSM", "TRUVISION", "Netvu observer", "Continuum", "Tournique"],
        "Travaux": ["Nettoyage", "Intervention IT", "Préparation d'évènements"],
        "Accident": ["Chutes", "Intérieur d'OTA", "Extérieur d'OTA"],
        "Incident": ["Alarme CDS", "DG(B1)", "Alarme MSC", "Werehouse"],
        "Demande de sécurisation": ["Véhicules employé en mission", "Véhicules OTA", "Matériel OTA"]
    };

    function mettreAJourFamilleOptions() {
        const selectedCategorie = categorieSelect.value;
        if (selectedCategorie && optionsParCategorie[selectedCategorie]) {
            const familleOptions = optionsParCategorie[selectedCategorie];
            familleSelect.innerHTML = '';
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.setAttribute('hidden', true);
            defaultOption.setAttribute('disabled', true);
            defaultOption.setAttribute('selected', true);
            familleSelect.add(defaultOption);

            familleOptions.forEach(option => {
                const newOption = document.createElement('option');
                newOption.text = option;
                familleSelect.add(newOption);
            });
        }
    }

    categorieSelect.addEventListener('change', mettreAJourFamilleOptions);
    mettreAJourFamilleOptions();

    function filterFunction(that, event) {
        let input = $(that);
        let input_val = input.val().toUpperCase();
        let ul = input.next("ul");

        if (["ArrowDown", "ArrowUp", "Enter"].indexOf(event.key) != -1) {
            keyControl(event, ul);
        } else {
            ul.find("li").each(function() {
                let li = $(this);
                if (li.text().toUpperCase().indexOf(input_val) > -1) {
                    li.show();
                } else {
                    li.hide();
                }
            });

            ul.find("li").removeClass("selected");
            setTimeout(function () {
                ul.find("li:visible").first().addClass("selected");
            }, 100);
        }
    }

    function keyControl(e, ul) {
        let selected = ul.find("li.selected");
        if (e.key == "ArrowDown") {
            if (selected.length) {
                let nextVisible = selected.nextAll(":visible").first();
                if (nextVisible.length) {
                    selected.removeClass("selected");
                    nextVisible.addClass("selected");
                }
            } else {
                ul.find("li:visible").first().addClass("selected");
            }
        } else if (e.key == "ArrowUp") {
            if (selected.length) {
                let prevVisible = selected.prevAll(":visible").first();
                if (prevVisible.length) {
                    selected.removeClass("selected");
                    prevVisible.addClass("selected");
                }
            }
        } else if (e.key == "Enter") {
            if (selected.length) {
                let input = ul.prev("input");
                input.val(selected.text()).blur();
                onSelect(selected.text(), input);
            }
        }

        selected = ul.find("li.selected");
        if (selected.length) {
            selected[0].scrollIntoView({
                behavior: "smooth"
            });
        }
    }

    function onSelect(val, inputElement) {
        if (inputElement.val() !== val) {
            alert(val);
        }
    }

    $(".affecte input, .ouvert input, .operateur input").on("input", function(event) {
        filterFunction(this, event);
    });

    $(".affecte input, .ouvert input, .operateur input").focus(function () {
        let ul = $(this).next("ul");
        ul.show();
        ul.find("li").show();
    });

    $(".affecte input, .ouvert input, .operateur input").blur(function () {
        let that = this;
        setTimeout(function () {
            $(that).next("ul").hide();
        }, 300);
    });

    $("ul li").on("click", function () {
        let input = $(this).closest("ul").prev("input");
        input.val($(this).text()).blur();
        onSelect($(this).text(), input);
    });

    $("ul li").on("mouseenter", function () {
        $(this).siblings().removeClass("selected");
        $(this).addClass("selected");
    });
});
