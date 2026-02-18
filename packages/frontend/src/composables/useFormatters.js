/**
 * Composable pour les fonctions de formatage
 */

/**
 * Formate une date pour l'affichage compact (ex: "Jan. 2024")
 * @param {string} dateStr - Date au format ISO ou string
 * @returns {string} Date formatée
 */
export function formatDate(dateStr) {
  if (!dateStr || dateStr === 'N/A') return 'N/A'
  
  try {
    const date = new Date(dateStr)
    if (isNaN(date.getTime())) return dateStr
    
    const months = ['Jan.', 'Fév.', 'Mars', 'Avr.', 'Mai', 'Juin', 'Juil.', 'Août', 'Sept.', 'Oct.', 'Nov.', 'Déc.']
    const month = months[date.getMonth()]
    const year = date.getFullYear()
    
    return `${month} ${year}`
  } catch {
    return dateStr
  }
}

/**
 * Formate une plage de dates pour les expériences (ex: "2020-2022")
 * @param {string} debut - Date de début
 * @param {string} fin - Date de fin (optionnel)
 * @returns {string} Plage formatée
 */
export function formatDateRange(debut, fin) {
  if (!debut) return 'En cours'
  const year = debut.substring(0, 4) || debut
  return fin ? `${year}-${fin.substring(0, 4)}` : year
}

/**
 * Détermine l'icône appropriée pour un poste
 * @param {string} poste - Titre du poste
 * @returns {string} Emoji correspondant
 */
export function getExperienceIcon(poste) {
  if (!poste) return '💼'
  const lower = poste.toLowerCase()
  if (lower.includes('école') || lower.includes('étude')) return '🎓'
  if (lower.includes('stage') || lower.includes('alternance')) return '💼'
  return '🚀'
}
