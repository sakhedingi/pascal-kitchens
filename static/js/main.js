// Alert close buttons
document.addEventListener('DOMContentLoaded', function() {
    const closeButtons = document.querySelectorAll('.alert-close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });
});

// Utility: Format currency
function formatCurrency(amount) {
    return 'R ' + Math.round(amount || 0).toLocaleString('en-ZA', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

// Quote builder functions
function updateLineItemTotal(lineItemId, quantity, rate) {
    const total = quantity * rate;
    const element = document.querySelector(`[data-line-id="${lineItemId}"] .line-total`);
    if (element) {
        element.textContent = formatCurrency(total);
    }
}

function deleteLineItem(lineItemId) {
    if (confirm('Delete this line item?')) {
        const element = document.querySelector(`[data-line-id="${lineItemId}"]`);
        if (element) {
            element.remove();
            recalculateTotals();
        }
    }
}

function recalculateTotals() {
    // This would be called after line items change
    // Implementation depends on your specific quote totaling logic
    console.log('Totals recalculated');
}

// Export to PDF simulation (actual implementation would use a library)
function exportQuotePDF() {
    window.print();
}

// Send quote via email
function sendQuoteEmail(quoteId) {
    const email = prompt('Enter client email:');
    if (email) {
        fetch(`/api/quotes/${quoteId}/send-email`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email })
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                alert('Quote sent successfully!');
            } else {
                alert('Error sending quote');
            }
        });
    }
}
