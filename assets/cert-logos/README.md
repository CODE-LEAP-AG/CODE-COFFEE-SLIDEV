# Certification Issuer Logos Cache

Pre-seeded logos for common certification issuers in CODE COFFEE decks.

## Issuer Mapping

| Issuer Domain | Logo File | Certifications | Source |
|---------------|-----------|-----------------|--------|
| `microsoft.com` | `microsoft.com.png` | Azure Administrator, Azure Developer Associate, Azure DevOps Expert, Power Platform cert, Azure AI 102 | https://cdn.brandfetch.io/microsoft.com/w/400/h/400/theme/light/fallback/lettermark |
| `amazon.com` | `amazon.com.png` | AWS cert | https://cdn.brandfetch.io/amazon.com/w/400/h/400/theme/light/fallback/lettermark |
| `cncf.io` | `cncf.io.png` | CKA, CKAD, CKS, KCNA, KCNS (Kubernetes certs) | https://cdn.brandfetch.io/cncf.io/w/400/h/400/theme/light/fallback/lettermark |
| `angular.io` | `angular.io.png` | Angular cert | https://cdn.brandfetch.io/angular.io/w/400/h/400/theme/light/fallback/lettermark |
| `vuejs.org` | `vuejs.org.png` | Vue.js cert | https://cdn.brandfetch.io/vuejs.org/w/400/h/400/theme/light/fallback/lettermark |
| `scrum.org` | `scrum.org.png` | PSPO II, PSPO, Scrum Master | https://cdn.brandfetch.io/scrum.org/w/400/h/400/theme/light/fallback/lettermark |
| `istqb.org` | `istqb.org.png` | ISTQB Testing certs (QE, QA) | https://cdn.brandfetch.io/istqb.org/w/400/h/400/theme/light/fallback/lettermark |
| `unity.com` | `unity.com.png` | Unity certs | https://cdn.brandfetch.io/unity.com/w/400/h/400/theme/light/fallback/lettermark |
| `servicenow.com` | `servicenow.com.png` | ServiceNow, HRSD | https://cdn.brandfetch.io/servicenow.com/w/400/h/400/theme/light/fallback/lettermark |
| `elastic.co` | `elastic.co.png` | Elasticsearch cert | https://cdn.brandfetch.io/elastic.co/w/400/h/400/theme/light/fallback/lettermark |

## Usage

When building a cert slide, add the `issuer` field to your spec:

```json
{
  "type": "cert",
  "name": "Thinh Nguyen",
  "role": "GEDAT // Senior Developer",
  "cert_name": "AZ-104: Microsoft Azure Administrator",
  "issuer": "microsoft.com",
  "photo": "./photos/thinh.jpg"
}
```

The engine will look up `assets/cert-logos/microsoft.com.png`. If not found, it will attempt to fetch from brandfetch.

## Adding New Issuers

If you need a cert from an issuer not in this cache:

1. **Automatic fetch (on-demand):** When `build_person_deck.py` encounters an `issuer` field with no cached PNG, it will attempt to fetch from brandfetch.io. If the fetch succeeds, the logo is cached locally for future builds.
2. **Pre-seed the cache:** Run `scripts/seed_cert_logos.py` to populate all 10 standard issuers at once (requires internet access).
3. **Manual placement:** Download a square PNG (transparent bg, logo centered, ~400×400px) and save to `assets/cert-logos/<issuer-domain>.png`.
4. Update this README with the issuer mapping and source URL.

## Notes

- All logos are normalized to square PNGs (transparent padding, centered).
- Logo dimensions must match the cert placeholder: 1828602 × 1828602 EMU (≈5.1 cm × 5.1 cm).
- Source URLs point to brandfetch.io's public API; logos are cached locally to avoid network calls during builds.
- **Current cache status:** Empty (pre-seed script available). On-demand fetch via build_person_deck.py works, but is rate-limited by brandfetch API redirects. User can manually place PNGs or wait for lazy loading on first cert build.
- **Lazy loading:** First cert slide build with an issuer will attempt to fetch from brandfetch. Subsequent builds use the cached file.
