# opensiddur.org posts

Source: https://github.com/aharonium/opensiddur.org, the monthly export of https://opensiddur.org
Issue: https://github.com/opensiddur/opensiddur-ai/issues/186

Each post the opensiddur.org importer takes is copied here verbatim from the export, stored
flat by post ID: `posts/<post_id>.json`. `categories.json` and `contributors_by_id.json` are
the export's own indexes. `manifest.json` records the export commit they were read at, the
categories selected, and each post's path in the export, `last_updated` and sha256.

Everything here is written by `opensiddur.importer.opensiddur_org.download` and is
regenerated from the export; edit nothing by hand. A post is rewritten only when its
`last_updated` changes, so a month in which the site was merely re-saved leaves no diff.

Each post is under the licence its `custom_fields.open_content_license` names. The
importer's `licence_decisions.yaml` records which of those licences may be imported. The
export's category and contributor indexes are under CC BY-SA 4.0.

The selection is currently the pilot category, Ḥanukkah (183); see
`specs/OPENSIDDUR_ORG_IMPORT.md` in opensiddur-ai.
