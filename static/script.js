// Génération du camembert pour les résultats d'exploitation
const pieData = [{
    values: [success_count, fail_count],
    labels: ['Réussi', 'Échoué'],
    type: 'pie'
}];

const pieLayout = {
    title: 'Résultats d\'Exploitation CVE/CWE',
    height: 400,
    width: 500,
    margin: {
        l: 50,
        r: 50,
        b: 50,
        t: 50
    }
};

Plotly.newPlot('exploit-chart', pieData, pieLayout);
