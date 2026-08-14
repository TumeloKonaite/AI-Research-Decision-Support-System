import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import test from "node:test";

const source = (path) => readFileSync(fileURLToPath(new URL(`../${path}`, import.meta.url)), "utf8");

test("page declares loading, unavailable, pitch, bench, and provenance states", () => {
  const page = source("app/suggested-team/page.tsx");

  assert.match(page, /<SuggestedTeamPitch team=\{team\}/);
  assert.match(page, /<SuggestedTeamBench team=\{team\}/);
  assert.match(page, /<SuggestedTeamConsensusPanel team=\{team\}/);
  assert.match(page, /Suggested team unavailable/);
  assert.match(page, /kasifpl-team-layout/);
  assert.match(page, /useSelectedReport/);
  assert.match(page, /ReportLoadingState/);
});

test("current team UI exposes support, captaincy, bench roles, and provenance", () => {
  const player = source("components/kasifpl/components/PlayerTile.tsx");
  const bench = source("components/kasifpl/components/SuggestedTeamBench.tsx");
  const consensus = source("components/kasifpl/components/SuggestedTeamConsensusPanel.tsx");
  const styles = source("components/kasifpl/styles/kasifpl.css");

  assert.match(player, /player\.shirtNumber != null/);
  assert.doesNotMatch(player, /player\.number/);
  assert.match(player, /loading="lazy"/);
  assert.match(player, /alt=\{`\$\{player\.name\} headshot`\}/);
  assert.match(player, /onError=\{\(\) => setFailedImageUrl/);
  assert.match(player, /onError=\{\(\) => setFailedBadgeUrl/);
  assert.match(player, /kasifpl-player__fallback-position/);
  assert.match(player, /player\.teamBadgeUrl/);
  assert.match(player, /starterSupportCount/);
  assert.match(player, /squadSupportCount/);
  assert.match(player, /captainSupportCount/);
  assert.match(player, /viceCaptainSupportCount/);
  assert.match(player, /contributingExpertIds/);
  assert.match(player, /contributingRevealIds/);
  assert.match(bench, /Substitute goalkeeper/);
  assert.match(bench, /First/);
  assert.match(consensus, /Median XI support/);
  assert.match(consensus, /Split consensus/);
  assert.match(consensus, /contributingExperts/);
  assert.match(consensus, /excludedRevealCount/);
  assert.match(consensus, /authoritativeCataloguePositions/);
  assert.match(styles, /grid-template-columns: minmax\(0, 7fr\) minmax\(300px, 3fr\)/);
  assert.match(styles, /max-height: 700px/);
  assert.match(styles, /kasifpl-player--support-limited/);
  assert.match(styles, /kasifpl-player__headshot/);
  assert.match(styles, /object-fit: contain/);
});

test("suggested-player media fields remain optional", () => {
  const types = source("components/kasifpl/types.ts");

  for (const field of ["playerCode", "teamCode", "imageUrl", "teamBadgeUrl"]) {
    assert.match(types, new RegExp(`${field}\\?:`));
  }
});

test("player tiles render optional headshots and club badges", () => {
  const player = source("components/kasifpl/components/PlayerTile.tsx");

  assert.match(player, /showHeadshot \? \(/);
  assert.match(player, /src=\{player\.imageUrl \?\? undefined\}/);
  assert.match(player, /src=\{player\.teamBadgeUrl \?\? undefined\}/);
});

test("player tiles retain a position fallback when media is missing", () => {
  const player = source("components/kasifpl/components/PlayerTile.tsx");

  assert.match(player, /const showHeadshot = Boolean\(player\.imageUrl\)/);
  assert.match(player, /kasifpl-player__media--fallback/);
  assert.match(player, /\{player\.position\}/);
});

test("player tiles remove failed images without removing player details", () => {
  const player = source("components/kasifpl/components/PlayerTile.tsx");

  assert.match(player, /failedImageUrl !== player\.imageUrl/);
  assert.match(player, /failedBadgeUrl !== player\.teamBadgeUrl/);
  for (const detail of ["kasifpl-player__name", "kasifpl-player__support", "kasifpl-player__price", "kasifpl-player__badge"]) {
    assert.match(player, new RegExp(detail));
  }
});

test("exported pitch rejects incomplete and mismatched lineups", () => {
  const shared = source("components/kasifpl/components/_shared.tsx");

  assert.match(shared, /starters\.length !== 11/);
  assert.match(shared, /new Set\(starters\.map/);
  assert.match(shared, /gk\.length !== 1/);
  assert.match(shared, /team\.formation\.trim\(\) !== derivedFormation/);
});
