$(document).ready(function() {
    $(".ouvertpar").chosen();

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

    categorieSelect.addEventListener('change', mettreAJourFamilleOptions);

    mettreAJourFamilleOptions();
});
