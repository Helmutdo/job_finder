---
name: Pituto-AI Design System
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#494454'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#7b7486'
  outline-variant: '#cbc3d7'
  surface-tint: '#6d3bd7'
  primary: '#6b38d4'
  on-primary: '#ffffff'
  primary-container: '#8455ef'
  on-primary-container: '#fffbff'
  inverse-primary: '#d0bcff'
  secondary: '#0051d5'
  on-secondary: '#ffffff'
  secondary-container: '#316bf3'
  on-secondary-container: '#fefcff'
  tertiary: '#855000'
  on-tertiary: '#ffffff'
  tertiary-container: '#a76500'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e9ddff'
  primary-fixed-dim: '#d0bcff'
  on-primary-fixed: '#23005c'
  on-primary-fixed-variant: '#5516be'
  secondary-fixed: '#dbe1ff'
  secondary-fixed-dim: '#b4c5ff'
  on-secondary-fixed: '#00174b'
  on-secondary-fixed-variant: '#003ea8'
  tertiary-fixed: '#ffdcbb'
  tertiary-fixed-dim: '#ffb869'
  on-tertiary-fixed: '#2c1700'
  on-tertiary-fixed-variant: '#673d00'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
typography:
  display:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 48px
  xl: 80px
  gutter: 24px
  container-max: 1200px
---

## Brand & Style
The design system is engineered for a premium, AI-driven job search experience that prioritizes efficiency and executive-level professionalism. The brand personality is "The Quietly Powerful Assistant"—sophisticated, unobtrusive, and highly intelligent.

The visual style is **Premium Minimalism**. It utilizes high-ratio whitespace to reduce cognitive load during complex career transitions. By stripping away unnecessary ornamentation, the design system focuses the user's attention on AI-generated insights and high-value opportunities. The aesthetic leans into a modern SaaS vernacular: crisp edges, purposeful motion, and a surgical approach to layout.

## Colors
The palette is rooted in a "Studio White" environment to maximize clarity. 

- **Primary (Vibrant Violet):** Used exclusively for high-intent actions, AI-powered features, and active states. It signals intelligence and premium capability.
- **Secondary (Tech Blue):** Used for utility actions, links, and secondary interactive elements to provide a reliable, professional grounding.
- **Neutrals (Slate Grays):** A sophisticated scale of slates. Text is never pure black; #0f172a is used for headings to maintain a high-end, soft-contrast feel.
- **Accents:** Success, Warning, and Error states utilize desaturated versions of green, amber, and red to ensure they don't break the minimalist harmony.

## Typography
The system uses **Inter** for its neutral, highly legible character, ensuring that dense job descriptions and resumes remain scannable. For technical data and labels, **Geist** is introduced to provide a subtle "developer-tool" precision that reinforces the AI-powered nature of the product.

Hierarchy is established through weight and tight letter-spacing on larger headings. Body text utilizes generous line-height (1.6) to ensure long-form reading comfort.

## Layout & Spacing
This design system employs a **Fixed-Fluid Hybrid** grid. The main content container is capped at 1200px to maintain line-length readability. 

- **Grid:** A 12-column system is used for desktop, 8-column for tablet, and 4-column for mobile.
- **Rhythm:** An 8px linear scale governs all padding and margins. 
- **White Space:** Generous margins (48px+) are used between major sections to denote high-end quality and prevent the UI from feeling "cramped" or "budget."

## Elevation & Depth
Elevation is conveyed through **Tonal Layering** and **Subtle Shadows**, avoiding heavy skeuomorphism.

- **Level 0 (Floor):** Pure white (#ffffff) or ultra-light slate (#f8fafc) backgrounds.
- **Level 1 (Cards):** White background with a 1px border in #e2e8f0. No shadow in static state.
- **Level 2 (Hover/Focus):** A very soft, diffused shadow (0 10px 15px -3px rgba(0,0,0,0.05)) to suggest interactivity.
- **Level 3 (Overlays):** Modals and dropdowns use a medium shadow with a 15% backdrop blur (glassmorphism) on the overlay mask to maintain context.

## Shapes
The shape language is **Soft and Precise**. A 0.25rem (4px) base radius is used for small elements (checkboxes, tags), while 0.5rem (8px) is the standard for buttons and input fields. 

Large containers and cards use 0.75rem (12px) to provide a modern, approachable feel without appearing overly "bubbly" or juvenile. This balance maintains the professional integrity required for a high-end SaaS tool.

## Components

- **Buttons:** Primary buttons use a solid Vibrant Violet fill with white text. Secondary buttons use a transparent background with a Slate border. All buttons feature a subtle 150ms transition on hover, shifting opacity or border color slightly.
- **Inputs:** Fields use a 1px border (#e2e8f0). On focus, the border shifts to Tech Blue with a 2px soft outer glow (ring) of the same color at 20% opacity.
- **Cards:** Clean borders, no shadows by default. Content inside cards should follow the 24px padding rule.
- **Chips/Badges:** Small, 4px rounded shapes with low-saturation backgrounds (e.g., a light violet tint with darker violet text) for "AI-matched" or "Remote" tags.
- **Lists:** Clean rows separated by a 1px horizontal line (#f1f5f9). High-contrast typography for the job title, low-contrast for the company and location.
- **AI Insights Component:** A specialized card variant with a very subtle gradient border (Violet to Blue) to distinguish human-entered data from AI-generated suggestions.