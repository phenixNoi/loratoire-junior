# L’ORATOIRE – L’ORATEUR JUNIOR

Application Streamlit de préinscription.

## Déploiement gratuit
1. Créer un compte GitHub et un dépôt privé ou public.
2. Ajouter `app.py` et `requirements.txt`.
3. Sur https://share.streamlit.io/, connecter GitHub et déployer `app.py`.
4. Dans **Advanced settings → Secrets**, ajouter :
   ```toml
   ADMIN_PASSWORD = "choisir-un-mot-de-passe-long-et-unique"
   ```
5. Publier et partager l’URL générée.

## Important – stockage
Cette version de démonstration utilise SQLite dans le stockage local de l’application. Sur un hébergement gratuit, le stockage local peut être réinitialisé lors de certaines opérations ou redéploiements. Pour une utilisation réelle avec des données d’enfants, configurez un stockage persistant sécurisé (par exemple une base de données hébergée) avant de collecter des inscriptions. Ne publiez pas le fichier de base de données et protégez l’accès administrateur.

Les frais calculés :
- Intensive : 120 000 FCFA × 2 mois + 10 000 FCFA = 250 000 FCFA.
- Progressive : 70 000 FCFA × 3 mois + 10 000 FCFA = 220 000 FCFA.
