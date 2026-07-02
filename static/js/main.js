/* ==============================================================
   TastyBite - Custom JavaScript
   Small enhancements: auto-dismiss alerts, cart quantity controls,
   and confirm dialogs. Kept simple and beginner-friendly.
   ============================================================== */

document.addEventListener('DOMContentLoaded', function () {

    // ----------------------------------------------------------
    // Auto-dismiss Bootstrap alert messages after 4 seconds
    // ----------------------------------------------------------
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            // Use Bootstrap's Alert component to fade it out smoothly
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 4000);
    });

    // ----------------------------------------------------------
    // Cart quantity stepper buttons (+ / -)
    // These work with <input type="number"> fields in the cart page
    // that have the class "qty-input", and buttons with
    // data-action="increase" or data-action="decrease"
    // ----------------------------------------------------------
    document.querySelectorAll('[data-action="increase"]').forEach(function (button) {
        button.addEventListener('click', function () {
            const input = document.querySelector(
                `input.qty-input[data-item-id="${button.dataset.itemId}"]`
            );
            if (input) {
                input.value = parseInt(input.value) + 1;
            }
        });
    });

    document.querySelectorAll('[data-action="decrease"]').forEach(function (button) {
        button.addEventListener('click', function () {
            const input = document.querySelector(
                `input.qty-input[data-item-id="${button.dataset.itemId}"]`
            );
            if (input && parseInt(input.value) > 1) {
                input.value = parseInt(input.value) - 1;
            }
        });
    });

    // ----------------------------------------------------------
    // Confirm before removing an item from the cart
    // Applies to any form/button with class "confirm-remove"
    // ----------------------------------------------------------
    document.querySelectorAll('.confirm-remove').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const confirmed = confirm('Are you sure you want to remove this item from your cart?');
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });

});