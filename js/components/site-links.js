export async function initSiteLinks() {
  const response = await fetch('data/site.json');
  const site = await response.json();

  const linkMap = {
    youtube: site.links.youtube,
    'youtube-embed': site.prequel.youtubeEmbedUrl,
    fandomWiki: site.links.fandomWiki,
    deviantArt: site.links.deviantArt,
    facebook: site.links.facebook
  };

  document.querySelectorAll('[data-site-link]').forEach(el => {
    const key = el.getAttribute('data-site-link');
    const url = linkMap[key];
    if (!url) return;

    if (el.tagName === 'IFRAME') {
      el.src = url;
    } else {
      el.href = url;
    }
  });
}
