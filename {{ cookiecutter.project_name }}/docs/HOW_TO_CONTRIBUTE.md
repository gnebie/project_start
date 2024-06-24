# Comment contribuer à UserManager

Merci de votre intérêt pour la contribution à UserManager ! Nous accueillons les contributions de la communauté. Voici comment vous pouvez vous impliquer.

## Table des matières

1. [Code de Conduite](#code-de-conduite)
2. [Questions](#questions)
3. [Signaler un Bug](#signaler-un-bug)
4. [Proposer une Fonctionnalité](#proposer-une-fonctionnalité)
5. [Configurer l'Environnement de Développement](#configurer-lenvironnement-de-développement)
6. [Créer une Pull Request](#créer-une-pull-request)
7. [Ressources Supplémentaires](#ressources-supplémentaires)

## Code de Conduite

Ce projet adhère à un [code de conduite](./CODE_OF_CONDUCT.md) afin d'assurer un environnement respectueux et inclusif pour tous les contributeurs. Veuillez le lire et le respecter lors de votre participation au projet.

## Questions

Si vous avez des questions, n'hésitez pas à les poser en ouvrant une issue avec le label `question`.

## Signaler un Bug

Si vous trouvez un bug, veuillez ouvrir une issue en suivant ces étapes :

1. Vérifiez si le bug a déjà été signalé.
2. Si ce n'est pas le cas, créez une nouvelle issue et fournissez autant de détails que possible :
    - Version du logiciel
    - Environnement (système d'exploitation, version de Python, etc.)
    - Étapes pour reproduire le bug
    - Comportement attendu
    - Comportement réel

## Proposer une Fonctionnalité

Nous accueillons les suggestions d'améliorations et de nouvelles fonctionnalités. Pour proposer une fonctionnalité :

1. Ouvrez une issue avec le label `enhancement`.
2. Décrivez en détail la fonctionnalité proposée et expliquez pourquoi elle serait utile.

## Configurer l'Environnement de Développement

Pour commencer à contribuer, suivez ces étapes pour configurer votre environnement de développement :

1. Clonez le dépôt :
    ```sh
    git clone https://github.com/username/projetc-name.git
    cd projetc-name
    ```

2. Installez Poetry si ce n'est pas déjà fait :
    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3. Installez les dépendances :
    ```sh
    poetry install
    ```

4. Activez l'environnement virtuel :
    ```sh
    poetry shell
    ```

5. Exécutez les tests pour vérifier que tout fonctionne :
    ```sh
    poetry run pytest
    ```

## Créer une Pull Request

Nous vous recommandons de créer une branche pour vos modifications :

1. Créez une nouvelle branche :
    ```sh
    git checkout -b feature/nom-de-la-branche
    ```

2. Faites vos modifications.

3. Ajoutez et validez vos modifications :
    ```sh
    git add .
    git commit -m "Description des modifications"
    ```

4. Poussez vos modifications sur votre dépôt forké :
    ```sh
    git push origin feature/nom-de-la-branche
    ```

5. Ouvrez une pull request sur le dépôt principal.

Assurez-vous que votre pull request respecte les critères suivants :
- Le code suit les [normes de style du projet](./STYLE_GUIDE.md).
- Les tests sont ajoutés ou mis à jour pour couvrir les changements.
- La documentation est mise à jour si nécessaire.

## Ressources Supplémentaires

- [Documentation du projet](./docs)
- [Style Guide](./STYLE_GUIDE.md)
- [FAQ](./FAQ.md)

Merci encore pour votre intérêt et vos contributions à UserManager !