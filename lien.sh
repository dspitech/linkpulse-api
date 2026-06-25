#!/bin/bash

echo "Création de 30 liens raccourcis..."
echo ""

urls=(
  "https://pulsemetrics.io/produit-analytics"
  "https://pulsemetrics.io/produit-monitoring"
  "https://pulsemetrics.io/produit-alerts"
  "https://pulsemetrics.io/produit-dashboard"
  "https://pulsemetrics.io/produit-reports"
  "https://pulsemetrics.io/produit-api"
  "https://pulsemetrics.io/produit-mobile"
  "https://pulsemetrics.io/produit-cloud"
  "https://pulsemetrics.io/produit-enterprise"
  "https://pulsemetrics.io/produit-startup"
  "https://pulsemetrics.io/landing-produit"
  "https://pulsemetrics.io/landing-startup"
  "https://pulsemetrics.io/landing-enterprise"
  "https://pulsemetrics.io/landing-education"
  "https://pulsemetrics.io/landing-nonprofit"
  "https://pulsemetrics.io/promo-ete-2026"
  "https://pulsemetrics.io/promo-hiver-2026"
  "https://pulsemetrics.io/promo-printemps-2026"
  "https://pulsemetrics.io/promo-automne-2026"
  "https://pulsemetrics.io/promo-black-friday"
  "https://pulsemetrics.io/blog/guide-analytics"
  "https://pulsemetrics.io/blog/tutoriel-api"
  "https://pulsemetrics.io/blog/cas-client"
  "https://pulsemetrics.io/blog/meilleures-pratiques"
  "https://pulsemetrics.io/blog/securite-donnees"
  "https://pulsemetrics.io/newsletter-juin"
  "https://pulsemetrics.io/newsletter-juillet"
  "https://pulsemetrics.io/newsletter-aout"
  "https://pulsemetrics.io/newsletter-septembre"
  "https://pulsemetrics.io/newsletter-octobre"
)

count=1
success=0
failed=0

for url in "${urls[@]}"; do
  echo "[$count/30] $url"

  response=$(curl -s -X POST http://localhost:8001/api/links \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"$url\"}")

  if echo "$response" | grep -q '"code"'; then
    code=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['code'])" 2>/dev/null)
    short_url="http://localhost:8001/r/$code"
    echo "  $short_url"
    ((success++))
  else
    echo "   Échec"
    echo "  Réponse: $response"
    ((failed++))
  fi

  echo "---"
  ((count++))
  sleep 0.1
done

echo ""
echo " RÉSULTATS :"
echo "   Succès : $success/30"
echo "   Échecs : $failed/30"
echo ""
echo " Terminé !"
