export type ThemePresetId =
  | 'linear-pro'
  | 'ios-glass'
  | 'neobrutalism'
  | 'cyberpunk-hud'
  | 'win-xp'
  | 'terminal-tui'
  | 'hand-drawn';

export interface PresetTokens {
  containerClass: string;
  cardClass: string;
  headerClass: string;
  titleClass: string;
  subtitleClass: string;
  primaryButtonClass: string;
  secondaryButtonClass: string;
  badgeClass: string;
  inputClass: string;
  accentTextClass: string;
}

export interface ThemePreset {
  id: ThemePresetId;
  name: string;
  universe: string;
  tagline: string;
  description: string;
  tokens: PresetTokens;
  aiPromptSnippet: string;
  openSourceRefs?: string[];
}
