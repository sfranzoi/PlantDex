# backend/app/models.py
from pydantic import BaseModel
from typing import List, Optional


class PlantGuess(BaseModel):
    scientific_name: str
    common_names: List[str]
    score: float
    plantnet_id: Optional[str]
    thumbnails: List[str]
    related_images: List[str]


class AnalysisResult(BaseModel):
    top_guesses: List[PlantGuess]
    original_uploaded: Optional[str] = None  # future: store base64 or URL

    @staticmethod
    def from_plantnet(data: dict):
        results = data.get("results", [])
        top3 = results[:3]

        guesses = []
        for item in top3:
            species = item.get("species", {})
            sci = species.get("scientificNameWithoutAuthor", "Unknown")
            cmn = species.get("commonNames", [])
            id_ = species.get("gbifId", None)

            images = item.get("images", [])
            thumbs = [img["url"]["s"] for img in images if "url" in img]  # smallest imgs
            related = [img["url"]["m"] for img in images if "url" in img]  # for slideshow

            guesses.append(
                PlantGuess(
                    scientific_name=sci,
                    common_names=cmn,
                    score=item.get("score", 0.0),
                    plantnet_id=id_,
                    thumbnails=thumbs,
                    related_images=related
                )
            )

        return AnalysisResult(top_guesses=guesses)