var assert = require('assert');
// describe('Array', function() {
//   describe('#indexOf()', function() {
//     it('should return -1 when the value is not present', function() {
//       assert.equal([1, 2, 3].indexOf(4), -1);
//     });
//     it('should have value when present', () => {
//     	assert.equal([1, 2, 3].indexOf(2), 2);
//     });
//   });
// });
// onChange, the fields are stored in persistent storage
describe('persistent storage', function() {
	describe('claimField', function() {
		it('should store it\'s contents on change', function() {
			// focus on claim field
			// press three keys
			const claimTextbox = document.getElementById('formClaimInput');
			claimTextbox.value = 'clmVal';
			const obsVal = null;
			chrome.storage.local.get(['claimField'], function(result) {
	      obsVal = result.claimField;
	    });
			// assert contents of storage are the keys
			assert.equal('clmVal', obsVal);
			// clear storage
			chrome.storage.local.set({'claimField': fieldVal}, function() {
	      console.log('claimField is cleared');
	    });
		});
	});
	describe('linkField', function() {
		it('should store it\'s contents on change', function() {
			// focus on link field
			// press three keys
			// assert contents of storage are the keys
			// clear storage
		});
	});
	//after the popup is open, text is added, and it is closed, the popup should contain that text again once being opened
	// FIXME this test might not be nessasary
});
// data sent to server should contain link and claim
describe('communication with server', function() {
	describe('message sent to server', function() {
		it('should contain a link and a claim', function() {
			// enter data into claim and link fields
			// press cite
			// assert data sent to server contains the link and claim
		});
	});
	describe('message returned from server', function() {
		it('should contain a list of claims and links', function() {
			// send data to server
			// assert data returned has the correct json format
		});
	});
});
