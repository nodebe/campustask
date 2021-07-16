jQuery( document ).ready( function( $ ) {

	/* notifications */

	update_submit_button();

	$( '#bulk_select' ).on( 'change', function() {

		$( '.notification-select' ).prop( 'checked', this.checked );

		update_submit_button();

		// refresh the document
		$( document ).foundation();
	} );

	$( '.notification-select' ).on( 'change', function() {

		if ( $( '.notification-select' ).length === $( '.notification-select:checked' ).length )
			$( '#bulk_select' ).prop( 'checked', true );
		else
			$( '#bulk_select' ).prop( 'checked', false );

		update_submit_button();

		// refresh the document
		$( document ).foundation();
	} );

	function update_submit_button() {
		$( '#bulk_delete' ).prop( 'disabled', !$( '.notification-select:checked' ).length );
	}

	var deleteService = {
		'bind': function( element ) {
			$( element ).on( 'click', this.clickHandler );
		},

		'clickHandler': function( eventObj ) {
			eventObj.preventDefault();

			var element = $( this );
			var data = deleteService.parseURLVars( element.attr( 'href' ) );

			var ask = confirm( dasboardL10n.delete_service );
			if ( ask ) {
				$.post( Taskerr.ajaxurl, {
					action: 'taskerr_delete_service',
					_ajax_nonce: data[ 'ajax_nonce' ],
					delete: data[ 'delete' ]
				}, function( data ) {
					deleteService.ajaxResponse( data, element );
				}, "json" );
			}

			return false;
		},

		'ajaxResponse': function( data, element ) {

			$( '.notice' ).fadeOut( 'slow' );
			$( '#main:first-child' ).prepend( data.notice );
			$( document ).foundation( {
				topbar: {
					stickyClass: 'sticky-top-bar'
				}
			} );

			element.closest( 'article.service' ).remove();
		},

		'parseURLVars': function( url ) {
			var returnValues = [],
				hash;

			var keyValues = url.slice( url.indexOf( '?' ) + 1 ).split( '&' );
			for ( var i = 0; i < keyValues.length; i++ ) {

				strings = keyValues[ i ].split( '=' );
				returnValues.push( strings[ 0 ] );
				returnValues[ strings[ 0 ] ] = strings[ 1 ];

			}

			return returnValues;
		}

	};
	deleteService.bind( $( 'a.delete-service' ) );

} );
