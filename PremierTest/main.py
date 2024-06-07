from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Instanciation de l'application FastAPI
app = FastAPI()

# Modèle Pydantic pour les données de contact
class User(BaseModel):
    nom: str
    prenom: str
    adresse: str
    telephone: str
    email: str

# Gestion de la route racine
@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur mon API FastAPI"}

# Définition d'un endpoint GET pour récupérer des données
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Route pour créer un fichier de contact en utilisant une méthode POST
@app.post("/creer_fichier_contact/")
async def creer_fichier_contact(nom: str, prenom: str, adresse: str, telephone: str, email: str):
    nom_fichier = f"{nom}_{prenom}_contact.txt"
    contenu = f"""
    Nom: {nom}
    Prénom: {prenom}
    Adresse: {adresse}
    Téléphone: {telephone}
    Email: {email}
    """
    try:
        with open(nom_fichier, "w") as f:
            f.write(contenu)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du fichier: {str(e)}")
    return {"message": "Fichier de contact créé avec succès"}

# Route pour mettre à jour un fichier de contact en utilisant une méthode PUT
@app.put("/put_contact/{nom}/{prenom}/")
async def modifier_fichier_contact(nom: str, prenom: str, adresse: str, telephone: str, email: str):
    nom_fichier = f"{nom}_{prenom}_contact.txt"
    contenu = f"""
    Nom: {nom}
    Prénom: {prenom}
    Adresse: {adresse}
    Téléphone: {telephone}
    Email: {email}
    """
    try:
        with open(nom_fichier, "w") as f:
            f.write(contenu)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la modification du fichier: {str(e)}")
    return {"message": "Fichier de contact modifié avec succès"}

# Route pour supprimer un fichier de contact en utilisant une méthode DELETE
@app.delete("/delete_contact/{nom}/{prenom}/")
async def supprimer_fichier_contact(nom: str, prenom: str):
    nom_fichier = f"{nom}_{prenom}_contact.txt"
    try:
        import os
        os.remove(nom_fichier)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression du fichier: {str(e)}")
    return {"message": "Fichier de contact supprimé avec succès"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
