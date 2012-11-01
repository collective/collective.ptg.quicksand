from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.plonetruegallery.browser.views.display import BaseDisplayType
from collective.plonetruegallery.interfaces import IBaseSettings
from zope import schema
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.ptg.quicksand')

class IQuicksandDisplaySettings(IBaseSettings):
    quicksand_imagewidth = schema.Int(
        title=_(u"label_quicksand_imagewidth",
            default=u"Width of (each) image"),
        default=400,
        min=50)
    quicksand_imageheight = schema.Int(
        title=_(u"label_quicksand_imageheight",
            default=u"Height of (each) image"),
        default=260,
        min=50)
    quicksand_use_icons = schema.Bool(
        title=_(u"label_quicksand_use_icons",
            default=u"Use Thumbnail size instead of Size"),
        default=False)
    quicksand_style = schema.Choice(
        title=_(u"label_quicksand_style",
                default=u"What stylesheet (css file) to use"),
        default="style.css",
        vocabulary=SimpleVocabulary([
            SimpleTerm("style.css", "style.css",
                _(u"label_quicksand_style_default",
                    default=u"Default")),
            SimpleTerm("no_style.css", "no_style.css",
                _(u"label_quicksand_style_no",
                    default=u"No style / css file")),
            SimpleTerm("custom_style", "custom_style",
                _(u"label_quicksand_style_custom",
                    default=u"Custom css file")
            )
        ]))

    quicksand_custom_style = schema.TextLine(
        title=_(u"label_custom_style",
            default=u"Name of Custom css file if you chose that above"),
        default=u"mycustomstyle.css")


class QuicksandDisplayType(BaseDisplayType):
    name = u"quicksand"
    schema = IQuicksandDisplaySettings
    description = _(u"label_quicksand_display_type",
        default=u"Quicksand")

    def javascript(self):
        return u"""
 
<script type="text/javascript"
src="%(portal_url)s/++resource++ptg.quicksand/jquery.quicksand.js">
</script>
<script type="text/javascript">
  // Custom sorting plugin
  (function($) {
	$.fn.sorted = function(customOptions) {
		var options = {
			by: function(a) { return a.text(); }
		};
		$.extend(options, customOptions);
		$data = $(this);
		arr = $data.get();
		return $(arr);
	};
  });

  // DOMContentLoaded
  $(function() {
  
	// bind radiobuttons in the form
	var $filterType = $('#filter input[name="type"]');
	var $filterSort = '';
	
	// get the first collection
	var $quicksandbox = $('#quicksandbox');
	
	// clone quicksandbox to get a second collection
	var $data = $quicksandbox.clone();

	// attempt to call Quicksand on every form change
	$filterType.add($filterSort).change(function(e) {
		if ($($filterType+':checked').val() == 'all') {
			var $filteredData = $data.find('li');
		} else {
			var $filteredData = $data.find('li[class=' + $($filterType+":checked").val() + ']');
		}
	
	  // no sorting
		var $sortedData = $filteredData; 

		
		// finally, call quicksand
		$quicksandbox.quicksand($sortedData, {
			duration: 800,
			easing: 'easeInOutQuad'
		});
	});
  });
</script>
""" % {
    'speed': self.settings.duration,
    'portal_url': self.portal_url,
}

    def css(self):
        relpath = '++resource++ptg.quicksand'
        style = '%s/%s/%s' % (self.portal_url, relpath,
            self.settings.quicksand_style)

        if self.settings.quicksand_style == 'custom_style':
            style = '%s/%s' % (self.portal_url,
                self.settings.quicksand_custom_style)

        return u"""
</style>
<link rel="stylesheet" type="text/css" href="%(style)s"/>
""" % {
        'boxheight': self.settings.quicksand_imageheight,
        'boxwidth': self.settings.quicksand_imagewidth,
        'style': style
       }
QuicksandSettings = createSettingsFactory(QuicksandDisplayType.schema)
