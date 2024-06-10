document.addEventListener('DOMContentLoaded', function() {
    function updateFileName() {
        var input = document.getElementById('fileUpload');
        var fileName = input.files.length > 0 ? input.files[0].name : "Aucun fichier disponible";
        var maxLength = 20;  // Longueur maximale pour le nom de fichier affiché
    
        if (fileName.length > maxLength) {
            fileName = fileName.substring(0, maxLength) + "...";
        }
    
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

    /****************refresh button *******************************/
    const refreshButton = document.getElementById('refreshButton');

    refreshButton.addEventListener('click', function() {
        fetch('/all_reclamations')
            .then(response => response.json())
            .then(data => {
                const tbody = document.querySelector('tbody');
                tbody.innerHTML = '';
                if (data.length > 0) {
                    data.forEach(row => {
                        const tr = document.createElement('tr');
                        Object.values(row).forEach((value, index) => {
                            const td = document.createElement('td');
                            if (index === 4 || index === 5 || index === 7) {
                                const date = new Date(value);
                                const formattedDate = date.toISOString().slice(0, 10);
                                td.textContent = formattedDate;
                            } else {
                                td.textContent = value;
                            }
                            tr.appendChild(td);
                        });
                        tbody.appendChild(tr);
                    });
                } else {
                    const noResultsRow = document.createElement('tr');
                    const noResultsCell = document.createElement('td');
                    noResultsCell.setAttribute('colspan', '19');
                    noResultsCell.textContent = 'Aucun résultat trouvé';
                    noResultsRow.appendChild(noResultsCell);
                    tbody.appendChild(noResultsRow);
                }
            })
            .catch(error => console.error('Error fetching data:', error));
    });    
    

    /****************ouvre le tableau dans une nouvelle fenetre */
    const table = document.querySelector('table');

    table.addEventListener('dblclick', function() {
        const tbody = document.querySelector('tbody');
        if (tbody.children.length === 0 || tbody.children[0].children[0].textContent === 'Aucun résultat trouvé') {
            const newWindow = window.open('', '_blank');
            const newDocument = newWindow.document.open();

            const htmlContent = `
                <!DOCTYPE html>
                <html lang="fr">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Tableau</title>
                    <link rel="stylesheet" href="/static/style.css">
                </head>
                <body>
                    <p>Aucun résultat trouvé</p>
                </body>
                </html>
            `;

            newDocument.write(htmlContent);
            newDocument.close();
        } else {
            let rowsHtml = '';
            table.querySelectorAll('tbody tr').forEach(row => {
                const id = row.cells[0].textContent;
                const titre = row.cells[1].textContent;
                const sites = row.cells[2].textContent;
                const actionEntreprise = row.cells[3].textContent;
                const dateOuverture = row.cells[4].textContent;
                const dateFin = row.cells[5].textContent;
                const operateur = row.cells[6].textContent;
                const echeance = row.cells[7].textContent;
                const etages = row.cells[8].textContent;
                const affecteA = row.cells[9].textContent;
                const priorite = row.cells[10].textContent;
                const acces = row.cells[11].textContent;
                const ouvertPar = row.cells[12].textContent;
                const description = row.cells[13].textContent;
                const status = row.cells[14].textContent;
                const categorie = row.cells[15].textContent;
                const famille = row.cells[16].textContent;
                const commentaire = row.cells[17].textContent;
                const fichier = row.cells[18].textContent;

                rowsHtml += `
                    <tr>
                        <td>${id}</td>
                        <td>${titre}</td>
                        <td>${sites}</td>
                        <td>${actionEntreprise}</td>
                        <td>${dateOuverture}</td>
                        <td>${dateFin}</td>
                        <td>${operateur}</td>
                        <td>${echeance}</td>
                        <td>${etages}</td>
                        <td>${affecteA}</td>
                        <td>${priorite}</td>
                        <td>${acces}</td>
                        <td>${ouvertPar}</td>
                        <td>${description}</td>
                        <td>${status}</td>
                        <td>${categorie}</td>
                        <td>${famille}</td>
                        <td>${commentaire}</td>
                        <td>${fichier}</td>
                        <td>
                            <button class="edit-button" data-id="${id}" data-status="${status}" data-current-status="${status}">Modifier</button>
                            <form class="edit-form" action="/update_status" method="post" style="display: none;">
                                <input type="hidden" name="recordId" value="${id}">
                                <input type="text" name="newStatus" value="${status}">
                                <input type="hidden" name="currentStatus" value="${status}">
                                <button type="submit">Mettre à jour</button>
                            </form>
                        </td>

                    </tr>
                `;
            });

            const newWindow = window.open('', '_blank');
            const newDocument = newWindow.document.open();

            const htmlContent = `
                <!DOCTYPE html>
                <html lang="fr">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Tableau</title>
                    <link rel="stylesheet" href="/static/style.css">
                </head>
                <body>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Titre</th>
                                <th>Sites</th>
                                <th>Action Entreprise</th>
                                <th>Date Ouverture</th>
                                <th>Date Fin</th>
                                <th>Opérateur</th>
                                <th>Échéance</th>
                                <th>Étages</th>
                                <th>Affecté À</th>
                                <th>Priorité</th>
                                <th>Accès</th>
                                <th>Ouvert Par</th>
                                <th>Description</th>
                                <th>Status</th>
                                <th>Catégorie</th>
                                <th>Famille</th>
                                <th>Commentaire</th>
                                <th>Fichier</th>
                                <th>Modifier Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${rowsHtml}
                        </tbody>
                    </table>
                    <script>
                        document.querySelectorAll('.edit-button').forEach(button => {
                            button.addEventListener('click', function() {
                                const form = this.nextElementSibling;
                                form.style.display = 'block';
                                this.style.display = 'none';
                            });
                        });
                    </script>
                </body>
                </html>
            `;

            newDocument.write(htmlContent);
            newDocument.close();
        }
    });



});