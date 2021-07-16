jQuery( document ).ready( function( $ ) {

	var favorites = {
		'bind': function( element ) {
			$( element ).on( 'click', this.clickHandler );
		},

		'clickHandler': function( eventObj ) {
			eventObj.preventDefault();

			var element = $( this );
			var data = favorites.parseURLVars( element.attr( 'href' ) );

			var icon = $( '.favorite-icon', element );
			icon.toggleClass( 'processing-favorite' );
			icon.text( 'Please wait' ); // @todo Needs translation

			$.post( Taskerr.ajaxurl, {
				action: 'taskerr_favorites',
				current_url: Taskerr.current_url,
				_ajax_nonce: data[ 'ajax_nonce' ],
				favorite: data[ 'favorite' ],
				post_id: data[ 'post_id' ]
			}, function( data ) {
				favorites.ajaxSuccess( data, element );
			}, "json" );

			return false;
		},

		'ajaxSuccess': function( data, element ) {

			$( '.notice' ).fadeOut( 'slow' );
			$( '#main:first-child' ).prepend( data.notice );
			$( document ).foundation( {
				topbar: {
					stickyClass: 'sticky-top-bar'
				}
			} );

			element.replaceWith( data.html );
			if ( data.redirect )
				return;

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
	favorites.bind( $( 'a.fave-button' ) );

	var taskActionButtons = {
		'bind': function( element ) {
			$( element ).on( 'click', this.clickHandler );
		},

		'clickHandler': function( eventObj ) {
			eventObj.preventDefault();

			var element = $( this ).parent();
			var data = taskActionButtons.parseURLVars( $( this ).attr( 'href' ) );

			$.post( Taskerr.ajaxurl, {
				action: 'taskerr_task_update',
				current_url: Taskerr.current_url,
				_ajax_nonce: data[ 'ajax_nonce' ],
				task_action: data[ 'task_action' ],
				task_id: data[ 'task_id' ]
			}, function( data ) {
				taskActionButtons.ajaxSuccess( data, element );
			} );

			return false;
		},

		'ajaxSuccess': function( data, element ) {
			element.html( data );
			if ( data.redirect )
				return;
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
	taskActionButtons.bind( $( 'a.task-button' ) );

	if ( $.fn.colorbox ) {
		$( "a[rel='colorbox']" ).colorbox( {
			transition: 'fade',
			current: '',
			slideshow: false,
			slideshowAuto: false,
			maxWidth: '100%',
			maxHeight: '100%',
			scalePhotos: true
		} );
	}

	$( ".attachements-slider figure" ).hover(
		function() {
			$( ".attachements-slider figure figcaption" ).slideUp();
		},
		function() {
			$( ".attachements-slider figure figcaption" ).slideDown();
		}
	);

	// Categories Toggle button
	$( ".cat-down" ).bind( "click", function( event ) {
		event.preventDefault();
		$( this ).parent().toggleClass( "expanded" );
		$( this ).find( "i" ).toggleClass( "genericon-collapse", "genericon-expand" ).toggleClass( "genericon-expand", "genericon-collapse" );
	} );

	// Set current tab
	if ( $( 'dl.tabs' ).find( 'dd.active' ).length === 0 ) {
		$( 'dl.tabs dd' ).first().addClass( 'active' );
	}
	if ( $( '.tabs-content' ).find( 'section.active' ).length === 0 ) {
		$( '.tabs-content section' ).first().addClass( 'active' );
	}
} );
