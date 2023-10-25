// notifications.js
$(document).ready(function () {
    // Obtenez la liste des engins nécessitant du carburant
    var engins_a_ravitailler = VotreAPIObtenirEnginsAvecNiveauCarburantFaible();

    // Vérifiez s'il y a des notifications à afficher
    if (engins_a_ravitailler.length > 0) {
        // Affichez un popup ou une alerte pour chaque notification
        engins_a_ravitailler.forEach(function (engin) {
            var message = engin.notification_message_ravitaillement();

            // Afficher le message dans une fenêtre modale Bootstrap
            $('#notificationModal .modal-body').html(message);
            $('#notificationModal').modal('show');
        });
    }
});
$(document).ready(function () {
    // Obtenez la liste des engins nécessitant du carburant
    var engins_maintenance = VotreAPIObtenirEnginsAvecNiveauCarburantFaible();

    // Vérifiez s'il y a des notifications à afficher
    if (engins_maintenance.length > 0) {
        // Affichez un popup ou une alerte pour chaque notification
        engins_maintenance.forEach(function (engin) {
            var message = engin.notification_message_maintenance();

            // Afficher le message dans une fenêtre modale Bootstrap
            $('#notificationModal .modal-body').html(message);
            $('#notificationModal').modal('show');
        });
    }
});
