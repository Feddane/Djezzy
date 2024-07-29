document.addEventListener('DOMContentLoaded', function() {
    function updateFileName() {
        var input = document.getElementById('fileUpload');
        var fileName = input.files.length > 0 ? input.files[0].name : "Aucun fichier disponible";
        var maxLength = 20;
    
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
        "Demande de sécurisation": ["Véhicules employé en mission", "Véhicules OTA", "Matériel OTA"],
        "Panne technique system": ["CCTV", "ATS8600", "SSM", "TRUVISION", "Netvu observer", "Continuum", "Tournique"],
        "Autres": [""]
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


    /****************Gerer les mois selectionnes************/
    const moisSelect = document.getElementById('mois');

    if (moisSelect) {
        moisSelect.addEventListener('change', function() {
            const selectedMonth = this.value;
            console.log('Selected month:', selectedMonth);

            if (selectedMonth !== "") {
                fetch(`/statistique/data?mois=${selectedMonth}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        if (response.headers.get('Content-Type').startsWith('application/json')) {
                            return response.json();
                        } else {
                            window.location.href = response.url;
                            return null;
                        }
                    })
                    .then(data => {
                        if (data) {
                            if (Object.keys(data).length === 0) {
                                window.location.href = '/empty';
                            } else {
                                window.location.href = '/statistique';
                            }
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching data:', error);
                    });
            } else {
                console.log('No month selected, showing general statistics.');
                updateGeneralStatistics();
            }
        });
    } else {
        console.error('Element with id "mois" not found.');
    }

    /*************categorie **************/
    const categorie = document.getElementById('categorie2');

    if (categorie) {
        categorie.addEventListener('change', function() {
            const selectedCategorie = this.value;
            console.log('Selected categorie:', selectedCategorie);

            if (selectedCategorie !== "") {
                fetch(`/statistique/data?categorie=${selectedCategorie}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        if (response.headers.get('Content-Type').startsWith('application/json')) {
                            return response.json();
                        } else {
                            window.location.href = response.url;
                            return null;
                        }
                    })
                    .then(data => {
                        if (data) {
                            if (Object.keys(data).length === 0) {
                                window.location.href = '/empty';
                            } else {
                                window.location.href = '/statistique';
                            }
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching data:', error);
                    });
            } else {
                console.log('No categorie selected, showing general statistics.');
                updateGeneralStatistics();
            }
        });
    } else {
        console.error('Element with id "categorie2" not found.');
    }

    
    function updateImage(id, base64Data) {
        const imgElement = document.getElementById(id);
        if (imgElement) {
            imgElement.src = `data:image/png;base64,${base64Data}`;
        } else {
            console.error(`Element with id "${id}" not found.`);
        }
    }
    
    function updateGeneralStatistics() {
        fetch('/statistique/data')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                if (response.headers.get('Content-Type').startsWith('application/json')) {
                    return response.json();
                } else {
                    throw new Error('Response is not JSON');
                }
            })
            .then(data => {
                updateImage('img_categorie', data.img_categorie);
                updateImage('img_famille', data.img_famille);
                updateImage('img_employe', data.img_employe);
                updateImage('img_priorite', data.img_priorite);
                updateImage('img_mois', data.img_mois);
            })
            .catch(error => {
                console.error('Error fetching general statistics:', error);
            });
    }

    function chargerListeDepuisFichier(url, selectorInput, selectorUL, onSelectCallback) {
        fetch(url)
            .then(response => response.text())
            .then(data => {
                const listeItems = data.trim().split('\n');
                const ulElement = document.querySelector(selectorUL);
                ulElement.innerHTML = '';
    
                listeItems.forEach(item => {
                    const li = document.createElement('li');
                    li.textContent = item.trim();
                    ulElement.appendChild(li);
    
                    li.addEventListener("click", function() {
                        let input = document.querySelector(selectorInput);
                        input.value = this.textContent.trim();
                        input.blur();
                        onSelectCallback(this.textContent.trim(), input);
                    });
    
                    li.addEventListener("mouseenter", function() {
                        this.parentElement.querySelectorAll("li").forEach(item => item.classList.remove("selected"));
                        this.classList.add("selected");
                    });
                });
            })
            .catch(error => console.error(`Erreur lors du chargement depuis ${url}:`, error));
    }

    function chargerOperateurs() {
        chargerListeDepuisFichier('/static/operateur.txt', '.operateur input', '.operateur ul', onSelect);
    }
    
    function chargerAffectes() {
        chargerListeDepuisFichier('/static/affecte_a.txt', '.affecte input', '.affecte ul', onSelect);
    }
    
    function chargerOuvertPar() {
        chargerListeDepuisFichier('/static/ouvert_par.txt', '.ouvert input', '.ouvert ul', onSelect);
    }
    
    chargerOperateurs();
    chargerAffectes();
    chargerOuvertPar();

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

    function onSelect(val, inputElement) {}

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

    /***********excel button******************************** */
    function toggleDateField() {
        const dateInput = document.getElementById('date_debut');
        const submitButton = document.getElementById('submitExcel');
        
        if (dateInput.style.display === 'none') {
            dateInput.style.display = 'block';
            submitButton.style.display = 'inline';
        } else {
            dateInput.style.display = 'none';
            submitButton.style.display = 'none';
        }
    }
    document.getElementById('excelButton').addEventListener('click', toggleDateField);



    $('#excelButton').on('click', function () {
        const dateOuverture = $('#date_debut').val();
    
        if (dateOuverture) {
            window.location.href = `/export_excel?date_ouverture=${dateOuverture}`;
    
            setTimeout(() => {
                $('#date_debut').val('');
                $('#date_debut').hide();
                $('#submitExcel').hide();
            }, 500);
        }
    });
    

    /****************refresh button *******************************/
    document.getElementById('refreshButton').addEventListener('click', function() {

        const currentPage = window.location.pathname;

        let fetchUrl;
        if (currentPage === '/historique' || currentPage === '/historique_supervisor') {
            fetchUrl = '/all_reclamations';
        } else if (currentPage === '/historique_user') {
            fetchUrl = '/all_reclamations_user';
        }

        if (fetchUrl) {
            fetch(fetchUrl)
                .then(response => response.json())
                .then(data => {
                    data.sort((a, b) => a.id - b.id);
        
                    let tbody = document.querySelector('table tbody');
                    
                    tbody.innerHTML = '';
        
                    data.forEach(reclamation => {
                        let newRow = document.createElement('tr');

                        newRow.innerHTML = `
                            <td>${reclamation.id}</td>
                            <td>${reclamation.titre}</td>
                            <td>${reclamation.sites}</td>
                            <td>${reclamation.action_entreprise}</td>
                            <td>${reclamation.date_ouverture}</td>
                            <td>${reclamation.date_fin}</td>
                            <td>${reclamation.operateur}</td>
                            <td>${reclamation.echeance}</td>
                            <td>${reclamation.etages}</td>
                            <td>${reclamation.affecte_a}</td>
                            <td>${reclamation.priorite}</td>
                            <td>${reclamation.acces}</td>
                            <td>${reclamation.ouvert_par}</td>
                            <td>${reclamation.description}</td>
                            <td>${reclamation.status}</td>
                            <td>${reclamation.categorie}</td>
                            <td>${reclamation.famille}</td>
                            <td>${reclamation.commentaire}</td>
                            <td>${reclamation.fichier}</td>
                        `;

                        tbody.appendChild(newRow);
                    });
                })
                .catch(error => console.error('Erreur lors du rafraîchissement des réclamations:', error));
        } else {
            console.error('URL de la page non reconnue.');
        }
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
                        <td>
                            <button class="edit-date-fin-button">Modifier</button>
                            <form class="edit-date-fin-form" action="/update_date_fin" method="post" style="display: none;">
                                <input type="hidden" name="recordId" value="${id}">
                                <input type="date" name="newDateFin" value="${dateFin}">
                                <button type="submit">Mettre à jour</button>
                            </form>
                        </td>
                        <td>${operateur}</td>
                        <td>${echeance}</td>
                        <td>${etages}</td>
                        <td>${affecteA}</td>
                        <td>${priorite}</td>
                        <td>${acces}</td>
                        <td>${ouvertPar}</td>
                        <td>${description}</td>
                        <td>${status}</td>
                        <td>
                            <button class="edit-button" data-id="${id}" data-status="${status}" data-current-status="${status}">Modifier</button>
                            <form class="edit-form" action="/update_status" method="post" style="display: none;">
                                <input type="hidden" name="recordId" value="${id}">
                                <div class="status">
                                    <label for="status">Status</label>
                                    <select id="status" name="newStatus">
                                        <option value="" hidden disabled selected></option>
                                        <option value="Actif">Actif</option>
                                        <option value="Résolu">Résolu</option>
                                        <option value="Fermé">Fermé</option>
                                        <option value="Inactif">Inactif</option>
                                    </select>
                                </div>
                                <input type="hidden" name="currentStatus" value="${status}">
                                <button type="submit">Mettre à jour</button>
                            </form>
                        </td>
                        <td>${categorie}</td>
                        <td>${famille}</td>
                        <td>${commentaire}</td>
                        <td>${fichier}</td>
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
                                <th>Modifier Date Fin</th>
                                <th>Opérateur</th>
                                <th>Échéance</th>
                                <th>Étages</th>
                                <th>Affecté À</th>
                                <th>Priorité</th>
                                <th>Accès</th>
                                <th>Ouvert Par</th>
                                <th>Description</th>
                                <th>Status</th>
                                <th>Modifier Status</th>
                                <th>Catégorie</th>
                                <th>Famille</th>
                                <th>Commentaire</th>
                                <th>Fichier</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${rowsHtml}
                        </tbody>
                    </table>
                    <script>
                        document.querySelectorAll('.edit-date-fin-button').forEach(button => {
                            button.addEventListener('click', function() {
                                const form = this.nextElementSibling;
                                form.style.display = 'block';
                                this.style.display = 'none';
                            });
                        });

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