/* BroService runtime configuration.
   Analytics is OFF while every ID below is empty: no script is loaded, no banner is shown,
   nothing is stored. To enable, paste the owner-approved IDs and redeploy.
   When enabled, measurement runs only after the visitor accepts the consent banner
   (Do Not Track / Global Privacy Control are treated as "declined").
   The privacy pages switch their wording automatically when an ID is set. */
window.BROSERVICE_CONFIG = {
  ga4MeasurementId: "",   // e.g. "G-XXXXXXXXXX"
  metaPixelId: ""         // e.g. "123456789012345"
};
