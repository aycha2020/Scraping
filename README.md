Ce projet consiste à construire un pipeline de data engineering pour les annonces immobilières d’Avito.ma. L’objectif est de transformer des données brutes issues du scraping en un système prêt pour l’analyse (Power BI) et le Machine Learning.

Le pipeline suit ces étapes :
Extraction → Staging → Nettoyage → Feature Engineering → Data Warehouse

Deux structures sont créées dans le Data Warehouse :

 BI Schema : modèle en étoile (Fact + Dimensions) pour l’analyse et les dashboards Power BI
 ML Schema : une table unique (OBT) contenant toutes les features pour le Machine Learning

Le projet inclut aussi :

Gestion des données (doublons, valeurs manquantes, outliers)
Respect de la conformité (pas de données personnelles, RGPD)
Automatisation via Docker
Logs et contrôle de qualité

 En résumé : c’est un pipeline complet, automatisé et industriel pour transformer des données immobilières en datasets exploitables pour la BI et le ML

